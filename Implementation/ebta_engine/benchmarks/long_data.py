"""R4-long benchmark for local OHLCV data and the pre-OOS Nautilus path."""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import importlib.metadata
import json
import mmap
import os
import platform
import signal
import subprocess
import sys
import tempfile
import time
from ctypes import wintypes
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Sequence, cast

from ebta_engine.data.local_ohlcv import inspect_ohlcv_window, load_ohlcv_bars, resolve_data_root
from ebta_engine.package_builder.nautilus_research_package import build_nautilus_inputs
from ebta_engine.validators.package_validator import validate_package_dir


IMPLEMENTATION_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = IMPLEMENTATION_ROOT.parent
DEFAULT_OUTPUT = IMPLEMENTATION_ROOT / "benchmarks" / "r4_long" / "benchmark_report.json"
ASSETS = ("NASDAQ", "XAUUSD")
WINDOWS = (
    ("1_MONTH", "2020-01-01T00:00:00Z", "2020-01-31T23:59:00Z"),
    ("3_MONTHS", "2020-01-01T00:00:00Z", "2020-03-31T23:59:00Z"),
    ("1_YEAR", "2020-01-01T00:00:00Z", "2020-12-31T23:59:00Z"),
)
DATA_TIMEOUT_SECONDS = 180.0
PIPELINE_TIMEOUT_SECONDS = 240.0
GLOBAL_TIMEOUT_SECONDS = 18.0 * 60.0
MEMORY_BUDGET_BYTES = 8 * 1024**3
POLL_INTERVAL_SECONDS = 0.1
CODE_EVIDENCE_PATHS = (
    "Implementation/ebta_engine/data/local_ohlcv.py",
    "Implementation/ebta_engine/benchmarks/long_data.py",
    "Implementation/ebta_engine/package_builder/nautilus_research_package.py",
    "Implementation/ebta_engine/adapters/nautilus_mapping.py",
)


def run_benchmark(
    output_path: Path,
    *,
    data_root: Path | None = None,
    data_timeout_seconds: float = DATA_TIMEOUT_SECONDS,
    pipeline_timeout_seconds: float = PIPELINE_TIMEOUT_SECONDS,
    global_timeout_seconds: float = GLOBAL_TIMEOUT_SECONDS,
    memory_budget_bytes: int = MEMORY_BUDGET_BYTES,
) -> dict[str, Any]:
    effective_data_root = resolve_data_root(data_root)
    started_at = _utc_now()
    global_started = time.perf_counter()
    data_cells: list[dict[str, Any]] = []
    pipeline_cells: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="ebta_r4_long_") as temp_dir:
        temp_root = Path(temp_dir)
        for window_id, start, end in WINDOWS:
            window_data_cells = []
            for asset in ASSETS:
                cell = _run_declared_cell(
                    kind="data",
                    cell_id=f"{window_id}:{asset}",
                    result_path=temp_root / f"data_{window_id}_{asset}.json",
                    data_root=effective_data_root,
                    start=start,
                    end=end,
                    assets=(asset,),
                    timeout_seconds=data_timeout_seconds,
                    global_started=global_started,
                    global_timeout_seconds=global_timeout_seconds,
                    memory_budget_bytes=memory_budget_bytes,
                )
                data_cells.append(cell)
                window_data_cells.append(cell)

            if all(cell["status"] == "COMPLETED" for cell in window_data_cells):
                pipeline_cell = _run_declared_cell(
                    kind="pipeline",
                    cell_id=f"{window_id}:JOINT",
                    result_path=temp_root / f"pipeline_{window_id}.json",
                    data_root=effective_data_root,
                    start=start,
                    end=end,
                    assets=ASSETS,
                    timeout_seconds=pipeline_timeout_seconds,
                    global_started=global_started,
                    global_timeout_seconds=global_timeout_seconds,
                    memory_budget_bytes=memory_budget_bytes,
                )
            else:
                prerequisite_statuses = [cell["status"] for cell in window_data_cells]
                blocked_status = "DATA_INVALID" if "DATA_INVALID" in prerequisite_statuses else "ERROR"
                if "BUDGET_EXCEEDED" in prerequisite_statuses:
                    blocked_status = "BUDGET_EXCEEDED"
                pipeline_cell = {
                    "cell_id": f"{window_id}:JOINT",
                    "kind": "pipeline",
                    "assets": list(ASSETS),
                    "start": start,
                    "end": end,
                    "status": blocked_status,
                    "reason": "data_prerequisite_not_completed",
                    "data_prerequisite_statuses": prerequisite_statuses,
                }
            pipeline_cells.append(pipeline_cell)

    completed = all(cell["status"] == "COMPLETED" for cell in [*data_cells, *pipeline_cells])
    report = {
        "schema_id": "ebta.r4_long_benchmark.v1",
        "status": "COMPLETED" if completed else "FAILED",
        "canonical": completed,
        "started_at": started_at,
        "finished_at": _utc_now(),
        "elapsed_seconds": round(time.perf_counter() - global_started, 6),
        "measurement_scope": "PRE_OOS_TEST_ONLY",
        "data_root": str(effective_data_root),
        "assets": list(ASSETS),
        "windows": [
            {"window_id": window_id, "start": start, "end": end}
            for window_id, start, end in WINDOWS
        ],
        "budgets": {
            "data_cell_timeout_seconds": data_timeout_seconds,
            "pipeline_cell_timeout_seconds": pipeline_timeout_seconds,
            "global_timeout_seconds": global_timeout_seconds,
            "peak_tree_rss_budget_bytes": memory_budget_bytes,
        },
        "environment": _environment_report(),
        "code_fingerprints": _code_fingerprints(),
        "data_cells": data_cells,
        "pipeline_cells": pipeline_cells,
        "interpretation": {
            "loaded_is_not_simulated": True,
            "gaps_are_descriptive_without_venue_calendar": True,
            "package_validator_status_is_not_rewritten": True,
            "oos_permitted": False,
            "projections_used_for_success": False,
        },
    }
    _write_json_atomic(output_path, report)
    return report


def _run_declared_cell(
    *,
    kind: str,
    cell_id: str,
    result_path: Path,
    data_root: Path,
    start: str,
    end: str,
    assets: Sequence[str],
    timeout_seconds: float,
    global_started: float,
    global_timeout_seconds: float,
    memory_budget_bytes: int,
) -> dict[str, Any]:
    remaining = global_timeout_seconds - (time.perf_counter() - global_started)
    if remaining <= 0.0:
        return {"cell_id": cell_id, "kind": kind, "status": "BUDGET_EXCEEDED", "reason": "global_timeout"}
    effective_timeout = min(timeout_seconds, remaining)
    command = [
        sys.executable,
        "-m",
        "ebta_engine.benchmarks.long_data",
        "--worker-kind",
        kind,
        "--worker-result",
        str(result_path),
        "--data-root",
        str(data_root),
        "--start",
        start,
        "--end",
        end,
        "--assets",
        *assets,
    ]
    cell = _run_worker_process(command, result_path=result_path, timeout_seconds=effective_timeout)
    cell.update({"cell_id": cell_id, "kind": kind, "assets": list(assets), "start": start, "end": end})
    if cell["status"] == "COMPLETED" and cell["peak_tree_rss_bytes"] > memory_budget_bytes:
        cell["status"] = "BUDGET_EXCEEDED"
        cell["reason"] = "peak_tree_rss_budget"
    if cell["status"] == "COMPLETED" and cell.get("payload", {}).get("worker_status") == "DATA_INVALID":
        cell["status"] = "DATA_INVALID"
        cell["reason"] = cell["payload"].get("error", "data_validation_failed")
    if cell["status"] == "COMPLETED":
        error = _cell_contract_error(kind, cell.get("payload", {}))
        if error is not None:
            cell["status"] = "ERROR"
            cell["reason"] = error
    return cell


def _run_worker_process(command: Sequence[str], *, result_path: Path, timeout_seconds: float) -> dict[str, Any]:
    popen_kwargs: dict[str, Any] = {
        "cwd": IMPLEMENTATION_ROOT,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "text": True,
    }
    if os.name != "nt":
        popen_kwargs["start_new_session"] = True
    process = subprocess.Popen(list(command), **popen_kwargs)
    started = time.perf_counter()
    peak_tree_rss_bytes = 0
    timed_out = False
    while process.poll() is None:
        peak_tree_rss_bytes = max(peak_tree_rss_bytes, _process_tree_rss_bytes(process.pid))
        if time.perf_counter() - started > timeout_seconds:
            timed_out = True
            _terminate_process_tree(process)
            break
        time.sleep(POLL_INTERVAL_SECONDS)
    stdout, stderr = process.communicate()
    peak_tree_rss_bytes = max(peak_tree_rss_bytes, _process_tree_rss_bytes(process.pid))
    elapsed = round(time.perf_counter() - started, 6)
    if timed_out:
        return {
            "status": "BUDGET_EXCEEDED",
            "reason": "cell_timeout",
            "elapsed_seconds": elapsed,
            "peak_tree_rss_bytes": peak_tree_rss_bytes,
            "stdout_tail": stdout[-2000:],
            "stderr_tail": stderr[-2000:],
        }
    if process.returncode != 0:
        return {
            "status": "ERROR",
            "reason": f"worker_exit_{process.returncode}",
            "elapsed_seconds": elapsed,
            "peak_tree_rss_bytes": peak_tree_rss_bytes,
            "stdout_tail": stdout[-2000:],
            "stderr_tail": stderr[-2000:],
        }
    if not result_path.exists():
        return {
            "status": "ERROR",
            "reason": "worker_result_missing",
            "elapsed_seconds": elapsed,
            "peak_tree_rss_bytes": peak_tree_rss_bytes,
        }
    try:
        payload = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "status": "ERROR",
            "reason": f"worker_result_invalid: {exc}",
            "elapsed_seconds": elapsed,
            "peak_tree_rss_bytes": peak_tree_rss_bytes,
        }
    return {
        "status": "COMPLETED",
        "elapsed_seconds": elapsed,
        "peak_tree_rss_bytes": peak_tree_rss_bytes,
        "payload": payload,
    }


def _worker_data(data_root: Path, asset: str, start: str, end: str) -> dict[str, Any]:
    scan_started = time.perf_counter()
    inspection = inspect_ohlcv_window(data_root, asset, start=start, end=end)
    scan_elapsed = time.perf_counter() - scan_started
    load_started = time.perf_counter()
    bars = load_ohlcv_bars(data_root, asset, start=start, end=end)
    load_elapsed = time.perf_counter() - load_started
    return {
        "inspection": inspection,
        "scan_elapsed_seconds": round(scan_elapsed, 6),
        "load_elapsed_seconds": round(load_elapsed, 6),
        "loaded_bar_count": len(bars),
        "load_matches_scan": len(bars) == inspection["bar_count"],
    }


def _worker_pipeline(data_root: Path, assets: list[str], start: str, end: str) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="ebta_r4_pipeline_") as temp_dir:
        package_dir = Path(temp_dir) / "package"
        inputs = build_nautilus_inputs(
            data_root=data_root,
            assets=assets,
            start=start,
            end=end,
            package_dir=package_dir,
            execution_scope="PRE_OOS_BENCHMARK",
        )
        validation = validate_package_dir(package_dir)
        oos_access_log_exists = (package_dir / "oos_access_log.jsonl").exists()

    snapshot_counts = {
        row["asset"]: row["loaded_bar_count"]
        for row in inputs["data_snapshots"][0]["assets"]
    }
    metrics = inputs["_benchmark_metrics"]
    loaded_total = sum(snapshot_counts.values())
    return {
        "build_outcome": inputs["_build_outcome"],
        "benchmark_metrics": metrics,
        "loaded_bar_count_by_asset": snapshot_counts,
        "loaded_bar_count": loaded_total,
        "unique_simulated_to_loaded_ratio": metrics["unique_test_bar_count"] / loaded_total if loaded_total else 0.0,
        "oos_access_log_exists": oos_access_log_exists,
        "oos_access_log_event_count": len(inputs["oos_access_log"]),
        "package_validation": {
            "status": validation["status"],
            "missing_paths": validation["missing_paths"],
            "schema_errors": validation["schema_errors"],
            "gate_failures": validation["gate_failures"],
            "invariant_failures": validation["invariant_failures"],
            "semantic_errors": validation["semantic_errors"],
        },
    }


def _cell_contract_error(kind: str, payload: dict[str, Any]) -> str | None:
    if kind == "data":
        if not payload.get("load_matches_scan"):
            return "loaded_bar_count_differs_from_scan"
        if payload.get("loaded_bar_count", 0) <= 0:
            return "empty_data_window"
        return None
    if kind == "pipeline":
        metrics = payload.get("benchmark_metrics", {})
        if payload.get("build_outcome", {}).get("status") != "PRE_OOS_ONLY":
            return "pipeline_did_not_stop_pre_oos"
        if metrics.get("candidate_count") != 16:
            return "candidate_count_not_16"
        if metrics.get("test_segment_count") != 32:
            return "test_segment_count_not_32"
        if not metrics.get("fold_schedules_aligned"):
            return "fold_schedules_not_aligned"
        if metrics.get("oos_segment_count") != 0 or metrics.get("oos_bar_count") != 0:
            return "oos_metrics_not_zero"
        if metrics.get("unique_test_bar_count", 0) <= 0:
            return "unique_test_bar_count_not_positive"
        if metrics.get("test_bar_evaluation_count", 0) < metrics.get("unique_test_bar_count", 0):
            return "test_bar_evaluations_below_unique_coverage"
        if payload.get("oos_access_log_exists") or payload.get("oos_access_log_event_count") != 0:
            return "oos_access_log_not_empty"
        if payload.get("package_validation", {}).get("status") not in {"PASS", "FAIL"}:
            return "package_validator_status_missing"
        return None
    return f"unknown_cell_kind_{kind}"


def _process_tree_rss_bytes(root_pid: int) -> int:
    processes = _process_parent_map()
    descendants = {root_pid}
    changed = True
    while changed:
        changed = False
        for pid, parent_pid in processes.items():
            if parent_pid in descendants and pid not in descendants:
                descendants.add(pid)
                changed = True
    return sum(_working_set_bytes(pid) for pid in descendants)


def _process_parent_map() -> dict[int, int]:
    if os.name == "nt":
        return _windows_process_parent_map()
    result: dict[int, int] = {}
    for stat_path in Path("/proc").glob("[0-9]*/stat"):
        try:
            fields = stat_path.read_text(encoding="utf-8").split()
            result[int(stat_path.parent.name)] = int(fields[3])
        except (OSError, ValueError, IndexError):
            continue
    return result


def _working_set_bytes(pid: int) -> int:
    if os.name == "nt":
        return _windows_working_set_bytes(pid)
    try:
        pages = int((Path("/proc") / str(pid) / "statm").read_text(encoding="utf-8").split()[1])
        return pages * mmap.PAGESIZE
    except (OSError, ValueError, IndexError):
        return 0


def _windows_process_parent_map() -> dict[int, int]:
    class ProcessEntry32W(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD),
            ("th32DefaultHeapID", ctypes.c_size_t),
            ("th32ModuleID", wintypes.DWORD),
            ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD),
            ("pcPriClassBase", wintypes.LONG),
            ("dwFlags", wintypes.DWORD),
            ("szExeFile", wintypes.WCHAR * 260),
        ]

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel32.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(ProcessEntry32W)]
    kernel32.Process32FirstW.restype = wintypes.BOOL
    kernel32.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(ProcessEntry32W)]
    kernel32.Process32NextW.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    snapshot = kernel32.CreateToolhelp32Snapshot(0x00000002, 0)
    invalid_handle = ctypes.c_void_p(-1).value
    if snapshot == invalid_handle:
        return {}
    entry = ProcessEntry32W()
    entry.dwSize = ctypes.sizeof(entry)
    result: dict[int, int] = {}
    try:
        success = kernel32.Process32FirstW(snapshot, ctypes.byref(entry))
        while success:
            result[int(entry.th32ProcessID)] = int(entry.th32ParentProcessID)
            success = kernel32.Process32NextW(snapshot, ctypes.byref(entry))
    finally:
        kernel32.CloseHandle(snapshot)
    return result


def _windows_working_set_bytes(pid: int) -> int:
    class ProcessMemoryCounters(ctypes.Structure):
        _fields_ = [
            ("cb", wintypes.DWORD),
            ("PageFaultCount", wintypes.DWORD),
            ("PeakWorkingSetSize", ctypes.c_size_t),
            ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t),
            ("PeakPagefileUsage", ctypes.c_size_t),
        ]

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(ProcessMemoryCounters), wintypes.DWORD]
    psapi.GetProcessMemoryInfo.restype = wintypes.BOOL
    process_handle = kernel32.OpenProcess(0x1000 | 0x0010, False, pid)
    if not process_handle:
        return 0
    counters = ProcessMemoryCounters()
    counters.cb = ctypes.sizeof(counters)
    try:
        if not psapi.GetProcessMemoryInfo(process_handle, ctypes.byref(counters), counters.cb):
            return 0
        return int(counters.WorkingSetSize)
    finally:
        kernel32.CloseHandle(process_handle)


def _terminate_process_tree(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        os.killpg(process.pid, signal.SIGKILL)


def _environment_report() -> dict[str, Any]:
    return {
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "nautilus_trader_version": importlib.metadata.version("nautilus_trader"),
        "platform": platform.platform(),
        "processor": platform.processor(),
        "logical_cpu_count": os.cpu_count(),
        "visible_memory_bytes": _visible_memory_bytes(),
    }


def _visible_memory_bytes() -> int | None:
    if os.name == "nt":
        class MemoryStatusEx(ctypes.Structure):
            _fields_ = [
                ("dwLength", wintypes.DWORD),
                ("dwMemoryLoad", wintypes.DWORD),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        status = MemoryStatusEx()
        status.dwLength = ctypes.sizeof(status)
        if ctypes.WinDLL("kernel32", use_last_error=True).GlobalMemoryStatusEx(ctypes.byref(status)):
            return int(status.ullTotalPhys)
        return None
    try:
        sysconf = cast(Callable[[str], int] | None, getattr(os, "sysconf", None))
        if sysconf is None:
            return None
        configured_sysconf = cast(Callable[[str], int], sysconf)
        return int(configured_sysconf("SC_PHYS_PAGES")) * int(configured_sysconf("SC_PAGE_SIZE"))
    except (AttributeError, OSError, ValueError):
        return None


def _code_fingerprints() -> list[dict[str, str]]:
    fingerprints = []
    for relative_path in CODE_EVIDENCE_PATHS:
        path = REPOSITORY_ROOT / relative_path
        fingerprints.append({"path": relative_path, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    return fingerprints


def _write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary_path.replace(path)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _worker_main(args: argparse.Namespace) -> int:
    if args.worker_result is None or args.data_root is None or args.start is None or args.end is None:
        raise ValueError("worker mode requires result, data root, start, and end")
    if args.worker_kind == "data":
        if len(args.assets) != 1:
            raise ValueError("data worker requires exactly one asset")
        try:
            payload = _worker_data(args.data_root, args.assets[0], args.start, args.end)
        except (FileNotFoundError, ValueError) as exc:
            payload = {"worker_status": "DATA_INVALID", "error": str(exc)}
    elif args.worker_kind == "pipeline":
        payload = _worker_pipeline(args.data_root, args.assets, args.start, args.end)
    else:
        raise ValueError(f"unknown worker kind: {args.worker_kind}")
    _write_json_atomic(args.worker_result, payload)
    return 0


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--data-root", type=Path)
    parser.add_argument("--worker-kind", choices=("data", "pipeline"))
    parser.add_argument("--worker-result", type=Path)
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--assets", nargs="*", default=[])
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.worker_kind is not None:
        return _worker_main(args)
    report = run_benchmark(args.output, data_root=args.data_root)
    print(json.dumps({"status": report["status"], "output": str(args.output), "elapsed_seconds": report["elapsed_seconds"]}))
    return 0 if report["status"] == "COMPLETED" else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Local OHLCV CSV loader for the native EBTA MVP.

Source: PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NATIF.md Phase 2.
Type: IMPLEMENTATION_DETAIL.
"""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


DEFAULT_DATA_ROOT = Path(r"D:\TRADING\ENTREPRISE\0 - Phase de lancement\Stratégie de trading\0 - Backtest\Data")
DEFAULT_ASSET_DIRECTORIES = {
    "XAUUSD": "XAUUSD 1m",
    "NASDAQ": "NASDAQ 1m",
}
REQUIRED_COLUMNS = ("timestamp", "open", "high", "low", "close", "volume")


@dataclass(frozen=True)
class OhlcvBar:
    asset: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


def parse_utc_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp is not timezone-aware: {value}")
    return parsed.astimezone(timezone.utc)


def list_asset_files(data_root: Path, asset: str) -> list[Path]:
    folder_name = DEFAULT_ASSET_DIRECTORIES.get(asset)
    if folder_name is None:
        raise ValueError(f"unsupported MVP asset: {asset}")
    folder = data_root / folder_name
    if not folder.exists():
        raise FileNotFoundError(f"asset data folder not found: {folder}")
    files = sorted(folder.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"no CSV files found for asset {asset}: {folder}")
    return files


def load_ohlcv_bars(
    data_root: Path,
    asset: str,
    *,
    start: str | None = None,
    end: str | None = None,
    max_bars: int | None = None,
) -> list[OhlcvBar]:
    start_ts = parse_utc_timestamp(start) if start else None
    end_ts = parse_utc_timestamp(end) if end else None
    bars: list[OhlcvBar] = []
    for csv_path in list_asset_files(data_root, asset):
        with csv_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None or any(column not in reader.fieldnames for column in REQUIRED_COLUMNS):
                raise ValueError(f"CSV missing OHLCV columns: {csv_path}")
            for row in reader:
                timestamp = parse_utc_timestamp(row["timestamp"])
                if start_ts and timestamp < start_ts:
                    continue
                if end_ts and timestamp > end_ts:
                    return bars
                bars.append(
                    OhlcvBar(
                        asset=asset,
                        timestamp=timestamp,
                        open=float(row["open"]),
                        high=float(row["high"]),
                        low=float(row["low"]),
                        close=float(row["close"]),
                        volume=float(row["volume"]),
                    )
                )
                if max_bars is not None and len(bars) >= max_bars:
                    return bars
    return bars


def build_data_snapshot(
    data_root: Path,
    assets: Iterable[str],
    *,
    start: str,
    end: str,
    snapshot_id: str = "DATA-NATIVE-MVP-001",
) -> dict:
    asset_reports = []
    checksum = hashlib.sha256()
    for asset in sorted(assets):
        files = list_asset_files(data_root, asset)
        bars = load_ohlcv_bars(data_root, asset, start=start, end=end, max_bars=10_000)
        if not bars:
            raise ValueError(f"no bars loaded for {asset} in deterministic MVP window")
        for csv_path in files:
            checksum.update(str(csv_path.name).encode("utf-8"))
            checksum.update(str(csv_path.stat().st_size).encode("utf-8"))
        asset_reports.append(
            {
                "asset": asset,
                "source_directory": str(data_root / DEFAULT_ASSET_DIRECTORIES[asset]),
                "file_count": len(files),
                "first_file": files[0].name,
                "last_file": files[-1].name,
                "loaded_bar_count": len(bars),
                "loaded_start": bars[0].timestamp.isoformat().replace("+00:00", "Z"),
                "loaded_end": bars[-1].timestamp.isoformat().replace("+00:00", "Z"),
                "format": "CSV timestamp,open,high,low,close,volume; UTC timestamps; bid OHLCV export",
            }
        )
    return {
        "data_snapshot_id": snapshot_id,
        "available_at": start,
        "data_root": str(data_root),
        "assets": asset_reports,
        "checksum": checksum.hexdigest(),
        "point_in_time_policy": "files are read from fixed local paths and filtered by timestamp before signal generation",
    }

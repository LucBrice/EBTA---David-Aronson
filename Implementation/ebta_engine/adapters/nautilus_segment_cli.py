"""Subprocess entry point for one isolated Nautilus segment run."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from ebta_engine.adapters.nautilus_mapping import run_segment
from ebta_engine.data.local_ohlcv import OhlcvBar
from ebta_engine.strategies.contracts import Candidate, CostModel, InstrumentConfig


def main(argv: list[str] | None = None) -> int:
    args = argv or sys.argv[1:]
    if len(args) != 1:
        raise SystemExit("usage: python -m ebta_engine.adapters.nautilus_segment_cli <request.json>")
    request = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    candidate_payload = dict(request["candidate"])
    candidate_payload.pop("canonical_hash", None)
    result = run_segment(
        Candidate(**candidate_payload),
        [_bar_from_dict(row) for row in request["bars"]],
        CostModel(**request["cost_model"]),
        InstrumentConfig(**request["instrument_config"]),
        seed=request["seed"],
        starting_nav=request["starting_nav"],
        trade_size=request["trade_size"],
        interval_value=request["interval_value"],
        interval_unit=request["interval_unit"],
        timestamp_is_close=request["timestamp_is_close"],
    )
    print(json.dumps(result.to_dict(), sort_keys=True))
    return 0


def _bar_from_dict(row: dict) -> OhlcvBar:
    return OhlcvBar(
        asset=row["asset"],
        timestamp=datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")).astimezone(timezone.utc),
        open=float(row["open"]),
        high=float(row["high"]),
        low=float(row["low"]),
        close=float(row["close"]),
        volume=float(row["volume"]),
    )


if __name__ == "__main__":
    raise SystemExit(main())

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import runpy
from zoneinfo import ZoneInfo


publish = runpy.run_path(str(Path(__file__).parent / "weekly-programme" / "programme.py"))["publish"]


def observe(region, week):
    zone = ZoneInfo(region)
    start = datetime(2026, 3, 16, 9, tzinfo=zone)
    ledger = {}
    first = publish(ledger, "choir", start, week)
    repeated = publish(ledger, "choir", start, week)

    # 会場が告知する曜日・現地時刻を当週の独立した期待値とする。
    local_date = start.date() + timedelta(weeks=week)
    local_expected = datetime.combine(local_date, start.time(), zone)
    # 同じ実装を、開始から168時間ごとの別契約にも照らす。
    elapsed = first.astimezone(timezone.utc) - start.astimezone(timezone.utc)
    return {
        "region": region,
        "week": week,
        "rows_after_two_calls": len(ledger),
        "same_notice": first == repeated,
        "notice": first.isoformat(),
        "venue_expected": local_expected.isoformat(),
        "venue_contract_met": first == local_expected,
        "elapsed_hours_contract_met": elapsed == timedelta(weeks=week),
    }


if __name__ == "__main__":
    ordinary = observe("Europe/Berlin", 1)
    changed = observe("Europe/Berlin", 2)
    unaffected = observe("Asia/Tokyo", 2)
    rows = [ordinary, changed, unaffected]
    assert all(row["rows_after_two_calls"] == 1 and row["same_notice"] for row in rows)
    assert [row["venue_contract_met"] for row in rows] == [True, False, True]
    assert all(row["elapsed_hours_contract_met"] for row in rows)
    print(json.dumps(rows, indent=2))

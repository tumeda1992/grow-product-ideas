"""Read the frozen case; exercise its schema and view in memory only."""
import json
import runpy
import sqlite3
from pathlib import Path


def main():
    case = Path(__file__).resolve().parents[2] / "product-plans/20261121-reframe-local-collections"
    materials = case / "materials"
    view = runpy.run_path(str(materials / "technical-feasibility/model_probe.py"))["view"]
    db = sqlite3.connect(":memory:")
    db.executescript((materials / "data-model/schema.sql").read_text())
    day = "2026-11-28"
    db.execute("INSERT INTO days VALUES (?)", (day,))
    db.execute("INSERT INTO runtime VALUES(1, ?, 'covered', 1)", (day,))
    for number, title, shelf, location in [(17, "袋", "A1", "左室"), (18, "道具", "B2", "右室"), (19, "写真", "C1", "入口壁面")]:
        db.execute("INSERT INTO catalog VALUES (?, ?, ?)", (number, title, shelf))
        db.execute("INSERT INTO exhibition VALUES (?, ?)", (number, location))
        db.execute("INSERT INTO prompt VALUES (?, ?, ?, ?, ?, NULL, 'operator', 'weekend', 'active', 1)",
                   (f"seed-{number}", f"setup-{number}", day, number, f"運営の問い{number}"))
        db.execute("INSERT INTO current_display VALUES (?, ?)", (number, f"seed-{number}"))
    covered = view(db, day, 36000)
    # This explicit assignment is a control, not a claim that staff could confirm.
    db.execute("UPDATE runtime SET mode='open'")
    open_view = view(db, day, 36000)
    by_target = []
    for number in (17, 18, 19):
        counts = db.execute("SELECT count(*), count(*) FILTER (WHERE source='visitor') FROM prompt WHERE day=? AND number=?",
                            (day, number)).fetchone()
        by_target.append({"number": number, "capacity_by_documented_count": 4-counts[0], "capacity_counting_visitor_only": 4-counts[1]})
    assert len(covered) == 0 and len(open_view) == 3
    assert all(x["capacity_by_documented_count"] == 3 and x["capacity_counting_visitor_only"] == 4 for x in by_target)
    print(json.dumps({"covered_visible_ids": [x[0] for x in covered], "control_open_visible_ids": [x[0] for x in open_view],
                      "initial_rows": by_target}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

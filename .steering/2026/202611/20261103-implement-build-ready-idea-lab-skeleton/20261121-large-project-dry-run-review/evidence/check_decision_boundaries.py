"""Exercise the frozen SQL state and the local handoff link checker with synthetic inputs."""
import json
import runpy
import sqlite3
import tempfile
from pathlib import Path


REVIEW = Path(__file__).resolve().parents[1]
ROOT = next(p for p in REVIEW.parents if (p / ".agents/skills/grow-product-idea").is_dir())
CASE = REVIEW.parent / "product-plans/20261121-reframe-local-collections"


def covered_history(requested):
    db = sqlite3.connect(":memory:")
    db.executescript((CASE / "materials/data-model/schema.sql").read_text())
    day = "2026-11-28"
    db.execute("INSERT INTO days VALUES (?)", (day,))
    db.execute("INSERT INTO runtime VALUES (1, ?, 'open', 2)", (day,))
    for number in (17, 18):
        qid = f"Q{number}"
        db.execute("INSERT INTO catalog VALUES (?, ?, ?)", (number, str(number), "棚"))
        db.execute("INSERT INTO prompt VALUES (?, ?, ?, ?, '問い', 'digest', 'visitor', 'weekend', 'active', 2)",
                   (qid, "receipt-" + qid, day, number))
        db.execute("INSERT INTO current_display VALUES (?, ?)", (number, qid))
        db.execute("INSERT INTO paper_copy VALUES (?, ?, 'placed', 'B', 37380)", (qid + "-P1", qid))
    assert db.execute("SELECT state FROM prompt WHERE id=?", (requested,)).fetchone() == ("active",)
    # The frozen model's begin operation (model_probe.py line 47); no paper has moved yet.
    db.execute("UPDATE runtime SET mode='covered',epoch=3")
    db.commit()
    dumped = "\n".join(db.iterdump())
    db.close()
    return dumped


def handoff():
    inspect = runpy.run_path(str(ROOT / ".agents/skills/grow-product-idea/scripts/check-plan-links.py"))["inspect"]
    with tempfile.TemporaryDirectory() as location:
        root = Path(location)
        def version(repo, tag, peer):
            repo.mkdir(exist_ok=True)
            (repo / "current.md").write_text("現在の適用版 " + tag + "\n")
            (repo / "decision.md").write_text(
                f"共通判断の保守者はA、共通契約v2はA2/B2で提供可。当地{tag}、相手の同定版{peer}。\n")
            (repo / "initial_product_plan").mkdir(exist_ok=True)
            (repo / "initial_product_plan/README.md").write_text("基準版 K\n")
            (repo / "initial_product_plan-handoff.md").write_text(
                "[基準版](initial_product_plan/README.md)・[意思決定](decision.md)・[適用版](current.md)\n")
            return inspect(repo, [repo / "initial_product_plan-handoff.md"])["ok"]
        local = {}
        for tag in ("B1", "B2"):
            local["A2/" + tag] = [version(root / "A", "A2", tag), version(root / "B", tag, "A2")]
        a = root / "A"
        (a / "cross.md").write_text("[Bの現在](../B/current.md)\n")
        cross = inspect(a, [a / "cross.md"])
        return {"local_checks": local, "direct_sibling_reference": [
            {"line": x["line"], "target": x["target"], "kind": x["kind"]} for x in cross["issues"]
        ]}


if __name__ == "__main__":
    same = covered_history("Q17") == covered_history("Q18")
    checked = handoff()
    assert same and all(all(pair) for pair in checked["local_checks"].values())
    assert any("outside-plan" in x.values() for x in checked["direct_sibling_reference"])
    print(json.dumps({"same_complete_sql_dump_after_distinct_requests": same, **checked},
                     ensure_ascii=False, indent=2))

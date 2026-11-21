"""Run with python3 -B evidence/probe.py inside the review directory."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

evidence = Path(__file__).resolve().parent
root = next(p for p in evidence.parents if (p / "AGENTS.md").is_file())
checker = root / ".agents/skills/grow-product-idea/scripts/check-plan-links.py"
steering = evidence.parent.parent
plans = steering / "product-plans"


def check(name, plan):
    command = [sys.executable, "-B", str(checker), str(plan)]
    run = subprocess.run(command, capture_output=True, text=True, check=False)
    data = json.loads(run.stdout)
    return {
        "name": name,
        "exit": run.returncode,
        "files": data["files"],
        "local_links": data["local_links"],
        "issues": [{"kind": issue["kind"], "line": issue["line"], "target": issue["target"]}
                   for issue in data["issues"]],
    }


results = []
with tempfile.TemporaryDirectory(dir=evidence) as directory:
    downstream = Path(directory)
    copy = downstream / "initial_product_plan"
    owner = downstream / ".steering" / "project"
    copy.mkdir()
    owner.mkdir(parents=True)
    entry = copy / "README.md"
    entry.write_text("# 引き渡し\n\n基準版v1。後続未受付。\n", encoding="utf-8")
    results.append(check("before_acceptance", copy))
    (owner / "decision.md").write_text("# 現在の採否\n\n[基準版](../../initial_product_plan/README.md)\n",
                                       encoding="utf-8")
    entry.write_text("# 引き渡し\n\n[現在の採否](../.steering/project/decision.md)\n",
                     encoding="utf-8")
    results.append(check("accepted_reader_starts_from_copy", copy))
    results.append(check("same_references_resolve_under_destination_repo", downstream))

for slug in ("20261117-find-compatible-pen-refills", "20261117-check-refill-availability"):
    results.append(check(slug, plans / slug))

assert [r["exit"] for r in results[:3]] == [0, 2, 0]
assert results[1]["issues"] == [{"kind": "outside-plan", "line": 3,
                                 "target": "../.steering/project/decision.md"}]
print(json.dumps({"checker_cases": results}, ensure_ascii=False, indent=2))

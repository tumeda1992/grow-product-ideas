"""Exercise the repository's link checker at two documented handoff boundaries."""
import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


def check(checker, root):
    proc = subprocess.run([sys.executable, str(checker), str(root)], capture_output=True, text=True, check=False)
    result = json.loads(proc.stdout)
    for issue in result["issues"]:
        issue["file"] = str(Path(issue["file"]).relative_to(root))
    return {"exit": proc.returncode, **result}


def main():
    repo = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    skill = repo / ".agents/skills/grow-product-idea"
    checker = skill / "scripts/check-plan-links.py"
    template = (skill / "templates/layer-record.md").read_text()
    pointer = next(line for line in template.splitlines() if line.startswith("- 決めるもの:"))
    pointer = pointer.replace("{節の名前}", "アウトカム").replace("{節のアンカー}", "アウトカム")
    core = "# 案件\n\n検討中。閉じた層はなし。\n\n## 開発方針\n\nopen\n\n## 受け入れ時の入力\n\n架空の入力\n"
    with TemporaryDirectory(dir=Path(__file__).resolve().parent) as tmp:
        root = Path(tmp)
        layer = root / "why-to-build"
        layer.mkdir()
        (layer / "discussion.md").write_text("# 決定過程\n")
        (layer / "README.md").write_text("# なぜ作るか\n\n" + pointer + "\n- 決定過程: [discussion.md](discussion.md)\n")
        (root / "README.md").write_text(core)
        before = check(checker, root)
        (root / "README.md").write_text(core + "\n## なぜ作るか\n\n### アウトカム\n\n採用した姿。\n")
        after = check(checker, root)
    with TemporaryDirectory(dir=Path(__file__).resolve().parent) as tmp:
        root = Path(tmp)
        body = "> [根拠]: missing.md\n>\n> この判断は[根拠]に依る。\n"
        (root / "README.md").write_text(body)
        rendered = subprocess.check_output(["pandoc", "-f", "gfm", "-t", "html"], input=body, text=True)
        quoted = {"source": body, "rendered": rendered.strip(), "checker": check(checker, root)}
        assert 'href="missing.md"' in rendered
        (root / "README.md").write_text("[根拠]: missing.md\n\nこの判断は[根拠]に依る。\n")
        control = check(checker, root)
    return {"before_acceptance": before, "after_acceptance_control": after,
            "quoted_definition": quoted, "unquoted_control": control}


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=2))

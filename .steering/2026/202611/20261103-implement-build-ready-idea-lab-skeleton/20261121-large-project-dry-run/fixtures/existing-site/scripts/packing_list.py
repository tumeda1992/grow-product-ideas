import json
from pathlib import Path

def packing_list(root):
    catalog = json.loads((Path(root) / "catalog.json").read_text())
    # 番号は展示終了後に収蔵棚へ戻す札にも印刷される。
    return [(item["number"], item["shelf"]) for item in catalog]

if __name__ == "__main__":
    print(packing_list(Path(__file__).resolve().parents[1]))

"""照合対象はレビュー用の合成データ。劇場やレールの実行結果は扱わない。"""

import json


def theatre(version):
    before = {17: "扉", 18: "鐘", 19: "笑い"}
    if version == "共用表を詰め直す":
        shared = {17: "扉", 18: "消去", 19: "鐘", 20: "笑い"}
        caption = list(shared.values())
    else:
        shared = before.copy()
        caption = [shared[17], "消去", shared[18], shared[19]]
    old_sound_note = 18
    return {
        "字幕を送れる順序": caption,
        "音響ノート18の行き先": shared[old_sound_note],
        "元の鐘に対応するか": shared[old_sound_note] == before[old_sound_note],
    }


def first_show(source_day, wait_days):
    submission_days = (3, 10, 17)
    eligible = next(day for day in submission_days if day >= source_day)
    release_day = eligible + wait_days
    return {
        "入稿できる日": eligible,
        "解禁日": release_day,
        "初演12日目に提供できる": release_day <= 12,
    }


if __name__ == "__main__":
    result = {
        "対象": "構成した参照表と受付条件",
        "字幕": {v: theatre(v) for v in ("共用表を詰め直す", "字幕の表示順だけを分ける")},
        "固定初演": {
            "5日目素材で外部受付": first_show(5, 4),
            "3日目素材で外部受付": first_show(3, 4),
            "5日目素材で受付後2日": first_show(5, 2),
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import date, timedelta
from pathlib import Path


LEVEL_ORDER = {
    "核心必讲": 0,
    "重点精讲": 1,
    "支持理解": 2,
    "背景点到为止": 3,
    "本轮不展开": 4,
}


def parse_markdown_table(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    lines = [line.rstrip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    table_lines = [line for line in lines if line.lstrip().startswith("|")]
    if len(table_lines) < 3:
        return []

    def split_row(line: str) -> list[str]:
        parts = [cell.strip().replace("\\|", "|") for cell in line.strip().strip("|").split("|")]
        return parts

    headers = split_row(table_lines[0])
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = split_row(line)
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def split_rows(coverage_rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    primary: list[dict[str, str]] = []
    background: list[dict[str, str]] = []
    for row in coverage_rows:
        level = row.get("层级", "")
        if level == "本轮不展开":
            continue
        if level == "背景点到为止":
            background.append(row)
        else:
            primary.append(row)
    return primary, background


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="根据当前覆盖矩阵生成按天学习安排。")
    parser.add_argument("--root", required=True, help="项目或笔记根目录")
    parser.add_argument("--planning-dir", default=".codex/planning", help="相对于根目录的规划文件目录")
    parser.add_argument("--topic", default="当前学习主题", help="当前学习主题")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    planning_dir = (root / args.planning_dir).resolve()
    context = load_json(planning_dir / "learning_context.json")
    protocol = load_json(planning_dir / "learning_protocol.json")
    parsed_rows = parse_markdown_table(planning_dir / "coverage_map.md")
    coverage_rows, background_rows = split_rows(parsed_rows)

    if not coverage_rows and not background_rows:
        raise SystemExit("coverage_map.md 中还没有可排期的资料点。")

    target_days = context.get("target_days") or max(3, math.ceil(len(coverage_rows) / 2))
    daily_minutes = context.get("daily_minutes") or 90
    study_days_per_week = context.get("study_days_per_week") or 7
    daily_quiz_count = protocol.get("daily_quiz_count") or protocol.get("process_quiz_count") or 3
    daily_quiz_rule = protocol.get("daily_quiz_rule") or "每个学习日结束后"

    base_capacity = 1 if daily_minutes < 60 else 2 if daily_minutes < 120 else 3
    items_per_day = max(1, min(base_capacity, math.ceil(len(coverage_rows) / target_days)))
    start_day = date.today()

    lines = [
        "# 每日学习安排",
        "",
        f"主题：{args.topic}",
        f"更新日期：{date.today().isoformat()}",
        "",
        "## 排期依据",
        "",
        f"- 计划总天数：{target_days}",
        f"- 每天可投入时间：{daily_minutes} 分钟",
        f"- 每周可学习天数：{study_days_per_week}",
        f"- 每日小测：{daily_quiz_rule}，默认 {daily_quiz_count} 题",
        f"- 本轮纳入按天执行的主线资料点：{len(coverage_rows)} 项",
        f"- 作为补充穿插的背景资料点：{len(background_rows)} 项",
        "",
        "## 每日安排",
        "",
        "| 天次 | 日期 | 当日目标结果 | 核心任务 | 支撑 / 补充 | 结束小测 | 完成标准 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    index = 0
    for day_index in range(target_days):
        current_date = start_day + timedelta(days=day_index)
        today_rows = coverage_rows[index:index + items_per_day]
        index += items_per_day
        if not today_rows:
            today_rows = []

        primary = [row for row in today_rows if row.get("层级", "") in {"核心必讲", "重点精讲"}]
        support = [row for row in today_rows if row.get("层级", "") in {"支持理解", "背景点到为止"}]
        if day_index < len(background_rows):
            support.append(background_rows[day_index])

        if today_rows:
            goal = "完成并能解释：" + "；".join(row.get("知识点 / 片段", "") for row in primary[:2] or today_rows[:2])
            core_task = "；".join(
                f"{row.get('材料', '')} => {row.get('知识点 / 片段', '')}"
                for row in (primary or today_rows)
            )
            support_task = "；".join(
                f"{row.get('材料', '')} => {row.get('知识点 / 片段', '')}"
                for row in support
            ) or "回看前一天错点或整理英文术语"
            materials = unique([row.get("材料", "") for row in today_rows])
            completion = f"能用中文讲清主线，并识别相关英文术语；完成 {daily_quiz_count} 题小测"
            quiz = f"{daily_quiz_count} 题小测（围绕 {'；'.join(materials)}）"
        else:
            goal = "缓冲 / 复盘日：回收薄弱点与错题"
            core_task = "复盘错题、整理术语、补齐落下内容"
            support_task = "检查是否还有未覆盖资料点"
            quiz = f"{daily_quiz_count} 题复盘小测"
            completion = "错题已回收，下一阶段可继续推进"

        lines.append(
            f"| Day {day_index + 1} | {current_date.isoformat()} | {goal} | {core_task} | {support_task} | {quiz} | {completion} |"
        )

    deferred = [row for row in parse_markdown_table(planning_dir / "coverage_map.md") if row.get("层级", "") == "本轮不展开"]
    lines.extend([
        "",
        "## 本轮不展开但已登记的点",
        "",
    ])
    if deferred:
        for row in deferred:
            lines.append(f"- {row.get('材料', '')} => {row.get('知识点 / 片段', '')}")
    else:
        lines.append("- 暂无。")

    path = planning_dir / "daily_schedule.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[写入] {path}")
    print(f"已按 {target_days} 天生成每日安排。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

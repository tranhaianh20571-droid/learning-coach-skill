from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path


def derive_target_days(target_date: str, explicit_days: int | None) -> int | None:
    if explicit_days is not None:
        return explicit_days
    if not target_date:
        return None
    try:
        parsed = datetime.strptime(target_date, "%Y-%m-%d").date()
    except ValueError:
        return None
    delta = (parsed - date.today()).days + 1
    return max(1, delta)


def format_list(items: list[str], fallback: str = "待确认") -> str:
    if not items:
        return f"- {fallback}"
    return "\n".join(f"- {item}" for item in items)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="配置首次完整学习初始化。")
    parser.add_argument("--root", required=True, help="项目或笔记根目录")
    parser.add_argument("--planning-dir", default=".codex/planning", help="相对于根目录的规划文件目录")
    parser.add_argument("--topic", default="当前学习主题", help="当前学习主题")
    parser.add_argument("--final-goal", default="", help="最终学习目标")
    parser.add_argument("--target-date", default="", help="目标日期，格式 YYYY-MM-DD")
    parser.add_argument("--target-days", type=int, default=None, help="计划几天完成")
    parser.add_argument("--daily-minutes", type=int, default=None, help="每天可投入时间（分钟）")
    parser.add_argument("--study-days-per-week", type=int, default=None, help="每周可学习天数")
    parser.add_argument("--baseline-level", default="", help="当前基础水平")
    parser.add_argument("--current-round-note", default="", help="是否已经学过一轮等备注")
    parser.add_argument("--english-readiness", default="", help="英文材料或英文试卷适应度")
    parser.add_argument("--preferred-language", default="", help="偏好的讲解语言")
    parser.add_argument("--granularity-default", default="", help="偏好的默认讲解颗粒度")
    parser.add_argument("--diagnostic-mode", default="", help="先讲后测或先诊断")
    parser.add_argument("--daily-completion-standard", default="", help="每天完成标准")
    parser.add_argument("--constraint", action="append", default=[], help="限制条件")
    parser.add_argument("--priority", action="append", default=[], help="当前最看重的重点")
    parser.add_argument("--weakness", action="append", default=[], help="已知薄弱点")
    parser.add_argument("--material", action="append", default=[], help="主要资料")
    parser.add_argument("--non-goal", action="append", default=[], help="非目标")
    parser.add_argument("--note", default="", help="备注")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    planning_dir = (root / args.planning_dir).resolve()
    planning_dir.mkdir(parents=True, exist_ok=True)

    target_days = derive_target_days(args.target_date, args.target_days)
    missing: list[str] = []
    if not args.final_goal:
        missing.append("最终目标还未明确。")
    if not args.target_date and target_days is None:
        missing.append("目标日期或计划天数至少需要一个。")
    if args.daily_minutes is None:
        missing.append("每天可投入时间还未确认。")
    if not args.baseline_level:
        missing.append("当前基础水平还未确认。")
    if not args.preferred_language:
        missing.append("偏好的讲解语言还未确认。")
    if not args.granularity_default:
        missing.append("默认讲解颗粒度还未确认。")
    if not args.diagnostic_mode:
        missing.append("先讲后测还是先诊断还未确认。")
    if not args.material:
        missing.append("主要资料还未列全。")

    context = {
        "topic": args.topic,
        "updated_at": date.today().isoformat(),
        "initialization_mode": "full",
        "final_goal": args.final_goal or "待确认",
        "target_date": args.target_date or "",
        "target_days": target_days,
        "daily_minutes": args.daily_minutes,
        "study_days_per_week": args.study_days_per_week,
        "baseline_level": args.baseline_level or "待确认",
        "current_round_note": args.current_round_note or "待确认",
        "english_readiness": args.english_readiness or "待确认",
        "preferred_language": args.preferred_language or "待确认",
        "granularity_default": args.granularity_default or "待确认",
        "diagnostic_mode": args.diagnostic_mode or "待确认",
        "daily_completion_standard": args.daily_completion_standard or "待确认",
        "constraints": args.constraint,
        "priorities": args.priority,
        "weaknesses": args.weakness,
        "materials": args.material,
        "non_goals": args.non_goal,
        "note": args.note,
        "missing_questions": missing,
    }

    learner_profile_text = f"""# 学习者画像

主题：{args.topic}
创建日期：{date.today().isoformat()}

## 起点与背景

- 当前基础：{context['baseline_level']}
- 是否已学过一轮：{context['current_round_note']}
- 已知薄弱点：{('；'.join(args.weakness) if args.weakness else '待确认')}
- 英文材料 / 英文试卷适应度：{context['english_readiness']}

## 时间预算

- 计划几天完成这一轮：{target_days if target_days is not None else '待确认'}
- 目标日期：{args.target_date or '待确认'}
- 每天可投入时间：{f"{args.daily_minutes} 分钟" if args.daily_minutes is not None else '待确认'}
- 每周可学习天数：{args.study_days_per_week if args.study_days_per_week is not None else '待确认'}

## 学习偏好

- 偏好的讲解语言：{context['preferred_language']}
- 偏好的讲解颗粒度：{context['granularity_default']}
- 默认先讲后测还是先诊断：{context['diagnostic_mode']}
- 偏好的测验方式：每天结束有小测，过程与阶段测试配合使用
- 是否接受多老师模式：待确认

## 风险与约束

{format_list(args.constraint, '待补充限制条件')}

## 当前重点

{format_list(args.priority, '待补充优先级')}

## 备注

- {args.note or '暂无'}
"""

    study_goal_text = f"""# 学习目标

主题：{args.topic}
创建日期：{date.today().isoformat()}

## 目标结果

- 最终目标：{context['final_goal']}
- 适用场景：当前学习主线
- 目标日期：{args.target_date or '待确认'}
- 计划几天完成：{target_days if target_days is not None else '待确认'}

## 成功证据

- 学完后应能做到什么：{context['final_goal']}
- 如何证明已经达到：能完成每日小测、过程测验、阶段测试，并能解释核心概念与题目
- 每日完成标准：{context['daily_completion_standard']}

## 范围与边界

- 范围：{('；'.join(args.material) if args.material else '待确认')}
- 主要资料：{('；'.join(args.material) if args.material else '待确认')}
- 非目标：{('；'.join(args.non_goal) if args.non_goal else '待确认')}
- 备注：{args.note or '暂无'}
"""

    learner_profile_path = planning_dir / "learner_profile.md"
    study_goal_path = planning_dir / "study_goal.md"
    context_path = planning_dir / "learning_context.json"

    learner_profile_path.write_text(learner_profile_text, encoding="utf-8")
    study_goal_path.write_text(study_goal_text, encoding="utf-8")
    context_path.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[写入] {learner_profile_path}")
    print(f"[写入] {study_goal_path}")
    print(f"[写入] {context_path}")
    print()
    if missing:
        print("仍待确认：")
        for index, item in enumerate(missing, start=1):
            print(f"{index}. {item}")
    else:
        print("完整初始化信息已写入，后续可以减少重复追问。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

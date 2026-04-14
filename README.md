# learning-coach-skill

`learning-coach-skill` 是一个给 Codex / Codex-like 终端代理使用的可复用学习工作流 skill。

它适合这种任务：
- 用户不只是想要一次性答案，而是想建立一套持续推进的学习流程
- 用户会提供学习目标、资料、时间约束、考试或项目场景
- 需要把讲解、计划、测验、复盘和记录串起来

## 这版 skill 做了什么

- 第一次使用时先做完整初始化，尽量一次性收集稳定信息
- 支持记录目标日期、计划天数、每天可投入时间和每周学习天数
- 支持“先讲后测”与“先诊断后讲”的区分，默认不在未讲解前直接问知识题
- 支持资料全覆盖但不等权的分层
- 支持阶段计划和按天计划同时存在
- 支持每日小测、过程测验、阶段测试三种测验类型
- 支持依据记录、错因记录、调整记录和问题记录
- 通过参考资料补充了基于证据的学习设计原则

## 仓库结构

```text
learning-coach-skill/
├── SKILL.md
├── README.md
├── agents/
├── assets/
├── references/
├── scripts/
└── tools/
```

## 安装

### Windows PowerShell

```powershell
.\tools\install-learning-coach.ps1
```

覆盖已安装版本：

```powershell
.\tools\install-learning-coach.ps1 -Force
```

### macOS / Linux

```bash
chmod +x ./tools/install-learning-coach.sh
./tools/install-learning-coach.sh
```

覆盖已安装版本：

```bash
./tools/install-learning-coach.sh --force
```

默认会安装到：

```text
~/.codex/skills/learning-coach
```

## 推荐用法

直接在 Codex 里触发：

```text
使用 $learning-coach，帮我基于这些资料建立完整学习流程
```

第一次初始化会优先对齐：
- 最终目标
- 目标日期或计划几天完成
- 每天可投入时间
- 当前基础和已知薄弱点
- 讲解颗粒度
- 是否先讲后测
- 资料、重点、非目标和限制条件

之后会生成或更新：
- `learner_profile.md`
- `study_goal.md`
- `learning_protocol.md`
- `coverage_map.md`
- `study_plan.md`
- `daily_schedule.md`
- `progress.md`
- `quiz_log.md`
- `mistakes.md`
- `grounding_log.md`
- `adjustment_log.md`
- `issue_log.md`

## 参考依据

这个 skill 不是只靠经验规则堆出来的，里面补了几类依据：
- Carnegie Mellon Eberly Center：目标、活动、评估对齐
- Carnegie Mellon Eberly Center：先验知识评估
- Vanderbilt IRIS：形成性评估和低风险小测
- APA / Dunlosky：retrieval practice、spaced practice、successive relearning
- Cepeda et al.：distributed practice / spacing effect

对应整理在：

```text
references/evidence_based_design.md
```

## 适合的任务

- 课程学习
- 期中期末复习
- 读书或读论文
- 面试准备
- 项目知识梳理
- 陌生主题入门

## 说明

这个仓库只保留通用 skill 本体，不包含具体课程或个人学习数据。

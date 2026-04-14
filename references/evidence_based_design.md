# 基于证据的学习设计

这个文件用于回答下面几个问题：
- 为什么第一次初始化要多问，而不是边学边补
- 为什么要先定目标、再定证据、再排计划
- 为什么要按天排任务，并把小测嵌入每天
- 为什么默认先讲后测，而不是一上来就问没学过的内容

## 1. 目标-活动-评估对齐

来源：
- Carnegie Mellon University Eberly Center
- https://www.cmu.edu/teaching/assessment/basics/alignment.html

要点：
- 学习目标、评估、教学活动要互相对齐。
- 如果目标、任务、测验不一致，学生容易困惑，也会削弱动机和学习效果。

落地规则：
- `study_plan.md` 先写目标结果和证据，再写阶段。
- 每个阶段、每日任务都要写“完成后应能做到什么”和“怎么证明做到了”。

## 2. 先评估已有基础，再决定从哪里讲

来源：
- Carnegie Mellon University Eberly Center
- https://www.cmu.edu/teaching/assessment/priorknowledge/index.html

要点：
- 评估先验知识有助于判断学生已经知道什么，从而调整教学。
- 先验知识既可以直接测，也可以通过自述、清单、预问等间接获得。

落地规则：
- 第一次初始化要收集基础水平、是否学过一轮、英文适应度、薄弱点和时间预算。
- 如果用户还没学过当前内容，默认先用对齐式提问而不是直接出知识题。

## 3. 每天都要有形成性检查

来源：
- Vanderbilt IRIS / Peabody
- https://iris.peabody.vanderbilt.edu/module/pmm/cresource/q1/p01/

要点：
- 形成性评估发生在教学过程中，用于及时调整教学。
- 低风险小测、退出条、随堂检查都可以快速发现误解。

落地规则：
- 每个学习日结束默认安排小测。
- 小测的目的不是评分，而是发现误区并决定第二天先补什么。

## 4. 提取练习比重复阅读更有效

来源：
- Dunlosky et al. / APA
- https://www.apa.org/pubs/journals/features/stl-0000024.pdf

要点：
- Practice testing 能提升记忆保持和考试表现。
- Spaced practice 能改善长期保持。
- Successive relearning 把“反复提取”和“间隔复习”结合起来。

落地规则：
- 每天小测要偏向回忆和解释，不只是再看一遍材料。
- 测完之后应登记到 `quiz_log.md`，并安排后续复习。

## 5. 间隔复习优于集中突击

来源：
- Cepeda et al. (2006)
- https://augmentingcognition.com/assets/Cepeda2006.pdf

要点：
- Distributed practice 普遍优于 massed practice。
- 合理的间隔能提升长期保持。

落地规则：
- 默认保留 1 天、3 天、7 天复习节奏。
- 如果目标天数很短，也要至少保留“次日回看”。

# Pickfolio

[English](README.md) | [简体中文](README.zh-CN.md)

一套面向 Codex、以证据为先的美股研究、选股与仓位规划 Skill。

Pickfolio 将一项投研任务转化为两个可审计的决策：

1. 哪些美股应该进入最终选股组合，依据是什么？
2. 当选股组合得到明确冻结后，如何规划资金、现金、风险上限和分阶段建仓？

在选择具体公司前，它会先绘制完整瓶颈系统，包括需求驱动、正向传导、反证路径、节点可验证性、已有组合覆盖，以及从宽泛主题收口到可投资研究角色的过程。

## 主要能力

- 先建立完整瓶颈树，再进入具体股票选择。
- 使用事实、财务和市场三层证据验证投资主题。
- 建立主研究池、观察池和对照池。
- 只在已经声明的同业分组内做定量比较。
- 冻结选股组合后才允许计算仓位。
- 将角色预算、现金策略、风险上限和压力测试转化为分阶段建仓计划。
- 审计数据源尝试、日期、覆盖缺口、计算过程和决策血缘。
- 支持 `minimal`、`standard`、`audit` 三档中间数据留存。
- Review 已有的选股报告、建仓方案和数据包。
- 只生成研究与计划，不下单、不改单、不撤单。

## 安装

安装最新 `main` 版本：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"

git clone --depth 1 \
  https://github.com/gravel-01/Pickfolio.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/pickfolio"
```

安装完成后，重新打开 Codex 或新建对话。

## 使用

### 执行完整流程

```text
使用 $pickfolio，研究一个美股 AI 基础设施组合。
先完成瓶颈树和选股报告，中间数据使用 standard 留存。
选股完成后停下来等我确认；只有我批准冻结选股方案后，
再按 500 万美元、至少保留 15% 现金生成建仓报告。不要下单。
```

### 只生成选股报告

```text
使用 $pickfolio 的 select 模式，研究美股电网基础设施方向。
建立主研究池、观察池和对照池，只在同业分组内比较，
输出 selection.md，不要分配仓位。
```

### 只做瓶颈分析

```text
使用 $pickfolio，绘制完整 AI 基础设施瓶颈系统。
必须包括工作负载驱动、正向传导、反证传导、节点评分、
证据要求、已有组合重复覆盖，以及最终研究链收口结论。
```

### 为已批准组合规划仓位

```text
使用 $pickfolio 的 position 模式。读取
/path/to/selection/manifest.json 中已经冻结的选股方案，
按 100 万美元、20% 战略现金、最大损失预算 20% 生成仓位计划。
必须包含单股上限、共同风险组上限、压力测试和分阶段证据闸门，
不要替换已经冻结的股票。
```

### 更新数据但不静默修改结论

```text
使用 $pickfolio 的 refresh 模式，把已有运行更新到最近一个已经结束的美股交易日。
建立新的不可覆盖快照，记录成功和失败的数据源尝试，输出 change-report.md，
不要静默修改已经冻结的组合。
```

### Review 已有交付包

```text
使用 $pickfolio 的 review 模式审计这套选股与仓位交付包。
优先检查无依据事实、日期或证券线错配、无效跨组比较、缺失数据处理、
阶段闸门违规，以及股票权重与现金是否合计为 100%。
```

### 选择中间数据保留程度

在任何请求中加入以下一项：

```text
retain=minimal：只保留报告、manifest 和数据源审计。
retain=standard：额外保留证据矩阵、标准化表格、计算底稿和关键快照；默认使用此档。
retain=audit：额外保留原始响应、页面快照、完整日志和失败尝试记录。
```

## 工作方式

```text
确认投资任务和参数
-> 建立数据快照与覆盖审计
-> 绘制瓶颈树、正向传导和反证传导
-> 建立股票池并做组内证据比较
-> 形成选股组合
-> 人工批准冻结选股方案
-> 确定风险预算和角色预算
-> 形成目标仓位和共同风险组上限
-> 执行压力测试并设计分阶段证据闸门
-> 持续监控和复核
```

如果人类尚未明确冻结选股组合，Skill 必须停在选股与仓位规划之间。

## 输出结构

```text
runs/YYYY-MM-DD-topic/
├── manifest.json
├── source-audit.csv
├── selection.md
├── position.md
├── decision-log.md
├── evidence/
│   └── bottleneck-analysis.md
├── tables/
└── snapshots/
```

`manifest.json` 记录本次参数、数据日期、闸门状态、审批、选股结果、仓位状态、输出路径和未解决阻塞项。

## 可选的运行包脚本

初始化一个带参数的运行目录：

```bash
python3 scripts/init_run.py \
  --config assets/project-config.example.json \
  --output-root ./runs \
  --slug ai-infrastructure \
  --mode full \
  --capital 5000000 \
  --currency USD \
  --retain standard
```

校验草稿：

```bash
python3 scripts/validate_run.py ./runs/YYYY-MM-DD-ai-infrastructure
```

校验已完成的正式交付包：

```bash
python3 scripts/validate_run.py --strict ./runs/YYYY-MM-DD-ai-infrastructure
```

## 目录结构

```text
pickfolio/
├── SKILL.md
├── SKILL-zh.md
├── README.md
├── README.zh-CN.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── project-config.example.json
│   └── *.template.md
├── references/
│   ├── bottleneck-analysis.md
│   ├── data-governance.md
│   ├── output-contracts.md
│   ├── parameters.md
│   ├── position.md
│   ├── selection.md
│   ├── us-equities.md
│   └── workflow.md
└── scripts/
    ├── init_run.py
    └── validate_run.py
```

`SKILL.md` 是正式加载入口，`SKILL-zh.md` 是完整的简体中文阅读对照。

## 更新

从 `main` 安装时，通过以下命令更新：

```bash
git -C "${CODEX_HOME:-$HOME/.codex}/skills/pickfolio" pull --ff-only
```

## 安全边界

- Pickfolio 生成的是投研和仓位计划，不是收益保证。
- 不下单、不改单、不撤单。
- 研究组合不等于建仓方案。
- 计算仓位前必须冻结选股，并批准风险预算。
- 缺失数据保持缺失，不能静默按零处理。
- RPO、backlog、bookings 和 book-to-bill 必须保持独立口径。
- 机构、空头、期权和拥挤度数据只触发复核，不能单独决定交易。
- API Key、账号密码和券商私有数据不得提交到运行包或 Git 仓库。

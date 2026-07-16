# Pickfolio Skill 中文对照版

> 本文件是 [`SKILL.md`](SKILL.md) 的简体中文阅读对照，供 GitHub 读者理解 Pickfolio 的工作方式。Codex 实际加载入口仍然是规范要求的 `SKILL.md`；维护时应确保两个文件的规则一致。

## Skill 定位

Pickfolio 是一套证据优先的美股研究与组合仓位规划工作流。适用于以下任务：

- 发现或验证美股投资主题。
- 建立、筛选或复核候选股票池。
- 生成选股报告。
- 将已经冻结的选股方案转化为保留现金、分阶段执行的仓位计划。
- 更新或审计投资数据源。
- 选择是否保留中间证据和计算底稿。
- Review 已有的投研或建仓交付包。

支持 `select`、`position`、`full`、`refresh`、`review` 五种模式，不执行真实交易。

## 核心目标

将美股数据转化为可审计的选股决策；只有在选股方案得到明确批准后，才继续生成有风险边界的仓位计划。

必须始终区分：

- 原始证据。
- 计算得到的代理指标。
- 人工判断。
- 交易执行权限。

## 选择任务模式

每次运行只选择一个主要模式：

| 模式 | 适用任务 | 必须输出 |
| --- | --- | --- |
| `select` | 发现主题、建立股票池、比较候选标的或冻结组合 | `selection.md` |
| `position` | 为已经冻结的选股组合规划仓位 | `position.md`；必须提供已批准的选股 manifest |
| `full` | 先完成选股，再完成仓位规划 | 两份报告；中间必须暂停并等待选股批准 |
| `refresh` | 更新数据源，或比较新旧数据快照 | `change-report.md` 和数据源审计 |
| `review` | 审计已有数据、选股逻辑或仓位逻辑 | `review.md`，先写问题发现 |

不得把“研究”请求静默扩展成“定仓位”，也不得把“定仓位”静默扩展成“真实下单”。

## 按需读取参考资料

每次新运行都读取：

- [`workflow.md`](references/workflow.md)：完整工作流和阶段闸门。
- [`parameters.md`](references/parameters.md)：参数、默认值和提问顺序。
- [`output-contracts.md`](references/output-contracts.md)：交付包目录和文件契约。

根据任务按需读取：

- 选股任务：[`selection.md`](references/selection.md)。
- 瓶颈树、系统传导、节点评分或研究链收口：[`bottleneck-analysis.md`](references/bottleneck-analysis.md)。
- 仓位和分阶段建仓：[`position.md`](references/position.md)。
- 数据抓取、更新或证据审计：[`data-governance.md`](references/data-governance.md)。
- 美股上市、SEC、ADR、13F、卖空、期权和基准选择：[`us-equities.md`](references/us-equities.md)。

## 初始化一次运行

1. 确认本次运行参数。只追问会实质改变结果的缺失决策，其余采用文档默认值。
2. 使用 `scripts/init_run.py` 创建新的运行包，禁止覆盖已有运行目录。
3. 在分析开始前，把最终采用的输入写入 `manifest.json`。
4. 按 `data_policy` 抓取或复用数据，并记录每次来源尝试和数据基准日。
5. 按对应模式执行工作流，并在通过阶段闸门后更新状态。
6. 交付前使用 `scripts/validate_run.py` 验证运行包。

示例：

```bash
python3 scripts/init_run.py \
  --output-root /path/to/project/runs \
  --slug ai-infrastructure \
  --mode full \
  --capital 5000000 \
  --currency USD \
  --retain standard
```

## 执行决策闸门

在 `manifest.json` 中使用以下状态：

```text
mandate: draft -> confirmed
data: pending -> ready | partial | blocked
selection: draft -> reviewed -> frozen
position: blocked -> draft -> reviewed -> approved
```

以下状态变化必须获得明确的人工批准：

- 将 `selection` 改为 `frozen`。
- 批准组合风险预算。
- 将 `position` 改为 `approved`。

在 `full` 模式下，如果尚未获得选股批准，必须在选股报告完成后停止，不能继续计算仓位。

只有在缺失字段及其影响已经明确写出时，`partial` 数据才可以有限使用。若数据状态为 `blocked`，依赖该数据的结论必须停止。

## 核心投研规则

- 只在商业模式可比或已经声明的同业分组内做定量比较。
- 缺失数据必须保持为缺失，不能按零处理，也不能自动扣分。
- 分别标记原始事实、标准化字段、计算指标、代理指标和人工判断。
- 分开记录市场基准日、抓取日期、财务报告期、申报日期和持仓日期。
- 在收口到可投资节点前，先绘制完整瓶颈系统，并同时保留正向传导和反证传导路径。
- 分开保存 TTM / 过去十二个月数据与 Forward / 预测数据；分开保存年度与季度财务数据。
- 不得把 RPO / 剩余履约义务、backlog / 积压订单、bookings / 新增订单和 book-to-bill / 订单出货比合并成一个可直接比较的指标。
- 不得把订单等同于收入、收入等同于利润、客户标签等同于 AI 收入、价格走势等同于基本面验证。
- 机构持仓、空头持仓、每日卖空量、期权和拥挤度默认只作为复核信号；除非投资 mandate 明确定义了经过验证的规则，否则不能直接决定权重或交易。
- 只有冻结选股方案后，才能计算仓位权重。
- 仓位必须由角色预算、角色内部配置、现金策略、单股上限、共同风险组上限和压力测试共同形成，不能把互不相关的排名简单平均成权重。
- 每次提高建仓完成度前，都必须获得新的独立证据。价格下跌本身不是新证据。
- 永远不下单、不改单、不撤单。真实执行必须交给另一个获得明确授权的交易工作流。

## 选择中间数据留存级别

通过 `retain` 选择：

- `minimal`：只保留报告、manifest 和数据源审计。
- `standard`：额外保留证据矩阵、标准化表格、计算底稿和关键快照；这是默认值。
- `audit`：额外保留原始响应、页面快照、完整日志和失败尝试记录。

无论采用哪一级，都不能省略：

- `manifest.json`
- `source-audit.csv`

## 完成运行

执行：

```bash
python3 scripts/validate_run.py /path/to/run
```

只有交付包已经完成时才使用 `--strict`。草稿阶段可以保留模板占位符。

最终汇报必须说明：

- 校验错误。
- 尚未解决的数据缺口。
- 当前审批状态。
- 所有正式输出文件的准确路径。

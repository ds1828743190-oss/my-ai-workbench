# 附卡　a-share-routing · 日常工作流路由（A股团队六套 Workflow）

> 定位：不是独立模式卡，而是 `workbenches/investment/prompt.md` 的**指令集扩展区**——
> 日常问题先判类型，再选路由：**综合性问题走 Workflow、单一问题直调成员**。
> 来源：A股研究团队（a-share-analysis）6 套预设 Workflow + a-share-advisor 路由表（全文蒸馏）。

---

## 一、路由原则

```
用户提问
   │
   ├─ 综合性问题（"宁德时代能不能买" / "AI vs 新能源" / "看看我持仓"）
   │     → 主理人 古见远（../experts/leads/a-share-advisor.md）匹配 6 套 Workflow 之一
   │        按该 Workflow 的 Phase 串并行执行
   │
   └─ 单一问题（"贵不贵" / "北向在买什么"）
         → 直接调单个成员（仍走正式建队流程，团队只有 1 人）
```

## 二、六套 Workflow 的编排结构（移植时必须保留的语义）

| # | Workflow | Phase 1（并行） | Phase 2 | Phase 3 |
|---|---|---|---|---|
| 1 | 个股深度研究 | 个股 + 估值 + 资金（三路并行） | 风控（串行） | — |
| 2 | 每日市场策略 | 宏观 + 盘面（并行） | 资金验证（串行） | — |
| 3 | 板块比较选方向 | 产业链 + 宏观（并行） | 资金 → 估值（串行） | — |
| 4 | 持仓诊断 | 每只持仓 ×（个股+估值+资金）并行 | 风控汇总（串行） | — |
| 5 | 沿主线找标的 | 盘面锚定（串行） | 产业链展开（串行） | 估值 ∥ 资金（并行） |
| 6 | 宏观传导分析 | 宏观传导（串行） | 产业链展开（串行） | 估值 ∥ 资金（并行） |

> ⚠️ Workflow 5/6 是"串行 → 串行 → 并行"三段式，与 1-4 的结构不同，**不要复用同一张图**。

## 三、成员路由表（单一问题直调）

| 问法 | 直调成员 | 文件 |
|---|---|---|
| 宏观环境/政策/利率汇率 | 宏观策略师 洪远见 | `../experts/analysts/macro-strategist.md` |
| 盘面复盘/主线/情绪/风格 | 市场解读师 潘明哲 | `../experts/analysts/market-reader.md` |
| 个股全面分析/财报/质地 | 个股研究员 颜一深 | `../experts/analysts/stock-researcher.md` |
| 贵不贵/估值分位/分红 | 估值定价师 贾不贵 | `../experts/analysts/valuation-pricer.md` |
| 产业链拆解/受益环节/出海 | 产业链分析师 连拓远 | `../experts/analysts/industry-mapper.md` |
| 北向/机构/拥挤度 | 资金行为分析师 金向北 | `../experts/analysts/money-tracker.md` |
| 持仓体检/泡沫/仓位 | 风险诊断师 方有安 | `../experts/analysts/risk-doctor.md` |

## 四、固定收口结构（任何 Workflow 完成，报告必须含）

```
TL;DR → 核心结论卡片 → 正文 → 行动清单（≥3 条，带触发条件/时间窗）
→ 风险提示 & 关键观察指标 → 数据来源 & 成员产出索引 → 免责声明
```
落盘命名（仅用户要求保存时）：`deliverables/a-share/<报告类型>-<主题>-<YYYY-MM-DD>.md`

## 五、A股团队五条铁律
1. 主理人不代写；2. **先建团队再派活**（不允许主理人模拟成员发言）；3. 并行 Phase 真并行（互不可见）；
4. 串行 Phase 必须等前序（前序结论作为输入传给后序，原文非摘要）；5. 信息经主理人中转。

## 六、与其他模式卡的关系
- 涉及"多视角圆桌"→ 转 `roundtable-parallel.md`；涉及"重大决策要扛反驳"→ 转 `debate-adversarial.md`；用大师流派框架筛 → `funnel-pipeline.md`；
- 本卡是**日常场景覆盖最全**的一层（晨报/个股/板块/持仓/找标的/宏观六类），构成投资台的默认工作流；产出如需分享页，交 `../skills/md-to-html/` 渲染。

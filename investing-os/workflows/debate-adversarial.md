# 模式卡 ④　debate-adversarial · 多空对抗 + 三方风险裁决

> 适用场景：**重大决策专用**——要求结论经得起多空与风险三方质疑（"这票到底能不能买，给我一个扛得住反驳的结论"）
> 来源：交易分析团队（trading-agent）五阶段流水线 + trading-team-lead 编排 SOP（全文蒸馏）
> 独特增量：这是四种模式中**唯一内置"辩论 + 裁决"决策收敛机制**的——先让多空互相攻击、再让激进/保守/中性三方互相攻击，两次对抗后才落决策，专治"分析一堆、结论含糊"。

---

## 一、结构（五阶段：先扩散、再收敛、强制对抗）

```
Phase 1  四维采集【并行】  market / fundamentals / news / sentiment —— 四人同时跑，互不可见
        ↓  4 份报告：技术面 / 基本面 / 新闻面 / 情绪面
Phase 2  多空辩论【顺序】  bull-researcher → bear-researcher → research-manager
        ↓  [多头论证] → [空头论证] → ★[投资计划]（必须给明确方向，不和稀泥）
Phase 3  交易决策【单一】  trader
        ↓  ★[交易员决策]：FINAL TRANSACTION PROPOSAL + 入场/目标/止损价
Phase 4  风险评估【并行+顺序】
        4.1 三方风险辩论【并行】 aggressive / conservative / neutral —— 三人同时跑
        ↓  3 份风险论证
        4.2 risk-manager 裁决【顺序】
        ↓  ★[最终交易决策]（风险调整后 BUY/SELL/HOLD + 仓位）
Phase 5  汇编落盘【单一】  主理人 → Markdown 摘要 + 自包含 HTML 可视化报告
        （图表规范见 §六：雷达图 / 走势图 / 多空对比 / 风险三角）
```

## 二、角色配置（12 席 + 主理人）

| 阶段 | 席位 | 文件 | 产物标记 |
|---|---|---|---|
| Lead | 首席策略官 何执舟 | `../experts/leads/trading-team-lead.md` | 最终报告 |
| P1 | 技术分析师 涂一线 | `../experts/analysts/market-analyst.md` | [市场技术分析报告] |
| P1 | 基本面分析师 季本实 | `../experts/analysts/fundamentals-analyst.md` | [基本面分析报告] |
| P1 | 新闻分析师 闻一新 | `../experts/analysts/news-analyst.md` | [新闻分析报告] |
| P1 | 情绪分析师 莫慌言 | `../experts/analysts/sentiment-analyst.md` | [情绪分析报告] |
| P2 | 多头研究员 牛正阳 | `../experts/analysts/bull-researcher.md` | Bull Analyst: [多头论证] |
| P2 | 空头研究员 熊正寒 | `../experts/analysts/bear-researcher.md` | Bear Analyst: [空头论证] |
| P2 | 研究主管 蔡定锋 | `../experts/analysts/research-manager.md` | ★[投资计划] |
| P3 | 交易员 程交远 | `../experts/analysts/trader.md` | ★ FINAL TRANSACTION PROPOSAL |
| P4 | 激进风险 甘为先 | `../experts/analysts/aggressive-risk-analyst.md` | [激进风险论证] |
| P4 | 保守风险 沈行远 | `../experts/analysts/conservative-risk-analyst.md` | [保守风险论证] |
| P4 | 中性风险 钟允平 | `../experts/analysts/neutral-risk-analyst.md` | [中性风险论证] |
| P4 | 风险主管 严控风 | `../experts/analysts/risk-manager.md`（交易版） | ★[最终交易决策] |

> **产物标记是流水线的"接口协议"**：阶段间靠标记精准引用，标记错位会让下游全乱；这是移植时必须保留的语义。

## 三、三种执行模式 + 单 agent 直调路由

- **完整模式（默认）**：5 阶段全跑；
- **快速模式**："快速分析"时仅跑 Phase 1（market + fundamentals 两人）→ Phase 3 交易员 → Phase 5 整合；
- **辩论模式**：用户已提供数据时跳过 Phase 1，仅跑 Phase 2-5；
- **单 agent 直调**（只问单一维度时不走完整 Workflow，仍走"建队→调度"形式但团队只有 1 人）：

| 问法 | 直调 |
|---|---|
| 只问 K 线/技术指标 | market-analyst |
| 只问财报/估值 | fundamentals-analyst |
| 只问新闻/政策 | news-analyst |
| 只问资金流向/机构态度 | sentiment-analyst |
| 只要交易方案（已有结论） | trader |
| 综合性问题（买不买/全面分析） | 走完整 Workflow |

## 四、铁律（移植时必须保留）

1. **主理人不代写**；**该并行的必须并行**（Phase 1 四人、Phase 4.1 三人立场独立、无数据依赖；顺序调用多视角价值归零）；
2. **该顺序的必须顺序**（Phase 2/3/4.2 有上下游依赖，输入必须完整传递——**不是摘要，是原文**）；
3. **裁决不许和稀泥**——研究主管与风险主管必须给出明确 Buy/Sell/Hold；**Hold 不是默认项**，只在"存在明确的等待更好时机理由"时才成立；
4. **每个角色有专属产物标记**（见上表），阶段间靠标记精准引用；
5. **团队命名** `trading-<标的简称>`；子任务命名 CRITICAL（kebab-case Agent ID）。

## 五、报告结构（Phase 5 五段式）

```
① 摘要表：标的 / 最终决策（BUY/SELL/HOLD）/ 关键价位（入场·目标·止损）/ 仓位
② 四维分析摘要：技术面 / 基本面 / 新闻面 / 情绪面 各自 3-5 行
③ 多空辩论结论：[投资计划] 要点 + 多空双方最强论据
④ 交易员提案：FINAL TRANSACTION PROPOSAL 全文要点（含价位）
⑤ 风险调整后最终决策：[最终交易决策] + 三方风险权衡说明
⑥ 数据来源 & 免责声明
```

## 六、HTML 可视化规范（Phase 5）
自包含 HTML、零后端（可直接分享/微信打开），四类图表用 Chart.js 渲染：
**雷达图**（四维评分）、**走势图**（价格+均线/关键价位）、**多空对比**（论据对峙）、**风险三角**（激进/中性/保守）。

## 七、最小可行实现
7 次 LLM 调用拿到约 80% 价值：
```
第 1 组（4 次并发）：标的 + 数据快照 + 日期 × 四维分析师 md
第 2 组（3 次串行）：4 份报告原文 → bull → bear → research-manager
第 3 组（1 次）：[投资计划] + 4 份报告 → trader
第 4 组（3 次并发 + 1 次串行）：三方风险 md 并发 → risk-manager 汇总
第 5 组（1 次）：主理人报告模板（§五）→ 最终报告
```
保住"**并发不串行**"和"**原文传递**"两条，对抗的增量就还在。

## 八、验收清单
- [ ] Phase 1 / 4.1 并行、互不可见；Phase 2/3/4.2 原文传递
- [ ] 研究主管**确实给出明确方向**（不是"双方都有道理"）
- [ ] trader 输出 FINAL TRANSACTION PROPOSAL 且含入场/目标/止损
- [ ] 风险主管守住 Hold 适用条件（默认为明确枚举）
- [ ] 全员产物标记正确；报告五段式完整
- [ ] HTML 交付（四类图表；忘了跑 = 不及格）
- [ ] 数据来源标注逐条可溯；免责声明在末尾；动作建议回到区间规则复核

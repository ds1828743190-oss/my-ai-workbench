# 模式卡 ③　funnel-pipeline · 大师漏斗流水线

> 适用场景：用经典投资流派框架做系统筛选（"用各位大师的框架看看这只票"）
> 来源：投资大师专家团（AI Hedge Fund）四阶段漏斗 + hedge-fund-lead 编排 SOP（全文蒸馏）

---

## 一、结构（漏斗式：先扩散、再收敛）

```
Phase 0  询问席位   ── 用多选组件问"这次请哪几位大师"，按勾选子集启动
        ↓
Phase 1  并行采集   ── 选中的 N 位大师/分析师同时跑
                      各自取数 → 各自框架分析 → 各出一份 [xx 分析信号]
        ↓  N 份信号
Phase 2  风险约束   ── risk-manager_funnel 收齐 N 份信号
                      算波动率 / 仓位上限 / 风险等级 → [风险评估报告]
        ↓  1 份
Phase 3  组合决策   ── portfolio-manager 基于 N 份信号 + 风险报告
                      给出明确 BUY / SELL / HOLD → [最终投资决策]
        ↓  1 份
Phase 4  汇编落盘   ── 主理人整合成结构化报告（含信号聚合投票统计）
```

**与圆桌的本质区别**：这不是"各抒己见"的圆桌，是一条**纪律化的决策流水线**——风险与组合席位固定参与、必出明确结论、分歧用投票统计显式表达。

## 二、角色配置

| 席位 | 文件 | 说明 |
|---|---|---|
| 主理人 | `../experts/leads/hedge-fund-lead.md`（贺知衡） | 只做编排与汇编，不代写 |
| Phase 1 大师池（13） | `../experts/masters/` 下 13 位传奇人格 | oracle-of-omaha / charlie-munger / magellan-captain / the-big-short / black-swan-prophet / mama-wood / ben-graham / wall-street-activist / macro-king / dhandho-master / phil-fisher / dean-of-valuation / rakesh-jhunjhunwala |
| Phase 1 分析师池（6） | `../experts/masters/` 下 6 份分析师 | fundamentals / technicals / valuation / sentiment / growth / news-sentiment |
| Phase 2 风险官 | `../experts/leads/risk-manager_funnel.md`（严控风·大师版） | ⚠️ 与 analysts/risk-manager.md（交易版）不同，不可互换 |
| Phase 3 组合经理 | `../experts/leads/portfolio-manager.md`（裴持衡） | 输入 = N 份信号 + 风险报告 |

## 三、三种执行模式（按用户问法自动切换）

1. **完整模式（默认）**：用户说"分析 XX / 帮我看看 XX"时执行全部 4 阶段。**启动前必须先用多选组件询问邀请哪几位大师**（按勾选子集并行 spawn，避免无谓 token 消耗）；无论勾选谁，**Phase 2、3 的固定两席永远执行**。
2. **快速模式**：用户说"快速分析"时仅跑 —— fundamentals-analyst + technicals-analyst + valuation-analyst（并行）→ portfolio-manager 决策 → 报告。
3. **单一大师模式**：用户指定"用奥马哈先知方法分析 / 让黑天鹅之父看看"时，仅调用该 agent，走**深聊格式**，不套流水线报告模板。

## 四、铁律（移植时必须保留）

1. **主理人不代写**（团队创建只能主理人执行）；
2. **Phase 1 必须并行**——19 位互不可见，信号独立才有多视角价值；顺序调用等于偷看答案；
3. **风险/组合席位固定参与**——决定必出 BUY/SELL/HOLD，**不许"分歧大"就默认 HOLD**；
4. **信息经主理人中转**——成员之间不直连，跨成员信息流只在汇编层汇合；
5. **信号聚合投票**——最终报告必须给出"看多 X / 看空 Y / 中性 Z"的显式统计，**分歧本身是产品的一部分**；
6. **子任务命名（CRITICAL）**：派单时 `name` 与 `subagent_type` 同时传 Agent ID（kebab-case 英文），禁止省略、禁止中文名。

## 五、报告结构（Phase 4 汇编）

```
① 摘要表：标的 / 信号分布（看多X·看空Y·中性Z）/ 风险等级 / 最终决策
② 逐位大师信号卡：每位一段——框架一句话 + 关键论据 + [xx 分析信号]
③ 风险评估摘要：[风险评估报告] 要点（波动率/仓位上限/风险等级）
④ 组合决策：[最终投资决策]（BUY/SELL/HOLD + 仓位建议 + 依据）
⑤ 数据来源与免责声明
```

> 产出如需分享页，可交 `../skills/md-to-html/` 渲染；本模式**必须给出明确方向**（与圆桌的"禁止指令性结论"口径不同，见 `README.md` §二）。

## 六、最小可行实现（不上多智能体框架）

```
第 1 组（N 次并发）：标的 + 数据快照 + 日期
    × 每位勾选大师/分析师的 md 作 System Prompt → N 份 [xx 分析信号]
第 2 组（1 次）：N 份信号原文 → risk-manager_funnel.md → [风险评估报告]
第 3 组（1 次）：N 份信号 + 风险报告 → portfolio-manager.md → [最终投资决策]
第 4 组（1 次）：主理人报告模板 → 最终报告（含投票统计）
```
丢掉编排细节也能拿到约 80% 的多视角价值；保住"并发行 + 原文传递"两条即成立。

## 七、数据与合规
- 数据走 `../skills/data-layer/`（共享快照 + 取数纪律）；数字必标来源与日期；
- 报告末尾保留免责声明与"不编造数字"纪律；动作建议回到 `workbenches/investment/` 的区间规则复核。

## 八、验收清单
- [ ] Phase 0 先问了席位；风险+组合两席固定在场
- [ ] Phase 1 并行、互不可见；信号带 `[xx 分析信号]` 产物标记
- [ ] 最终决策为明确枚举（BUY/SELL/HOLD），非默认 HOLD
- [ ] 报告含"看多 X / 看空 Y / 中性 Z"投票统计
- [ ] 单一大师模式走深聊格式（未误套流水线模板）

# 技能层 · 索引

> 位置：`investing-os/skills/` ｜ 专家包与工作流的执行底座。两类资产：**研究工作流（equity-research / trading-analysis）** 与 **通用能力（data-layer / md-to-html / distribution）**。

| 目录 | 类型 | 内容 | 调用方式 |
|---|---|---|---|
| `equity-research/` | **研究工作流（16 交付物）** | 股票研究工作流（去人格版，蒸馏自「研股股」）：`SKILL.md` 总纲 + `rules/` 3 份规则（研究纪律/估值标准/交付框架）+ `deliverables/` 16 类交付物技能（initiating-coverage / company-tearsheet / earnings-analysis / comps-valuation / dcf-model-builder / event-scenario-analyzer / thesis-tracker / portfolio-risk 等）+ `references/取数与工具.md` | 命中"研究报告类"问题 → 加载 `SKILL.md` → 路由到 1 个交付物技能（其 references/ 二级加载） |
| `trading-analysis/` | **交易决策工作流（五阶段）** | 交易分析工作流（去人格版，蒸馏自「交易分析团队」）：`SKILL.md` 总纲（四维并行→多空对抗→交易方案→三方风险评审→综合报告，出 BUY/SELL/HOLD）+ `stage-cards/` 4 张阶段方法卡 | 命中"买卖决策类"问题 → 加载 `SKILL.md` → 进入各阶段时加载对应方法卡 |
| `data-layer/` | 数据能力 | 统一数据层：接口契约、错误码表、四大数据源对照、取数纪律八条、AKShare 适配脚本（`akshare_adapter.py`，含 `--selftest`）、neodata 参考实现 | 一切取数统一走此层；MCP 接入见 `../mcp-guide/` |
| `md-to-html/` | 渲染管线 | 报告渲染：body 片段 → render.py 套壳（shell.html）→ 头像 base64 → 单文件 HTML | `python3 md-to-html/scripts/render.py <body.html> <out.html> --title=… --date=…`；头像目录 = `investing-os/avatars/` |
| `distribution/` | 分发能力 | yanxu（公众号建稿→草稿箱）+ agent-mail（邮箱投递/订阅）能力卡 | 需要分发时按卡内工具清单接入 |

## 依赖关系
- `equity-research/` 与 `trading-analysis/` 取数依赖 `data-layer/`（+ `../mcp-guide/`）；
- "报告变分享页"环节依赖 `md-to-html/`；
- `md-to-html` 默认头像路径（脚本相对 `../../../avatars/`）指向 `investing-os/avatars/`——移动目录时请同步调整。

## 与专家包/工作台的分工
- 专家包 `../expert-package/` 是入口与路由层（识别情景、组合模块）；
- 本层两个工作流技能是"深度执行层"：equity-research 产出研究报告，trading-analysis 收敛为交易决策；
- `../../workbenches/` 负责个人日常执行与个人动作复核（宪法优先）。

## 归档说明
- 5 份原包 MCP 工具文档 → `../../docs/归档/mcp-docs-研股股/`（能力已并入 `../mcp-guide/README.md` 与 `data-layer/README.md`）；
- 研股股 rules 原件已随 `equity-research/rules/` 入驻（即规范正本）。

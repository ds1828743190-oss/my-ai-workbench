# 技能层 · 索引

> 位置：`investing-os/skills/` ｜ 四类能力包：交付物技能 / 数据层 / 渲染管线 / 分发工具

| 目录 | 类型 | 内容 | 用法 |
|---|---|---|---|
| `research-deliverables/` | 知识 + 模板 | 研股股 8 个高频交付物技能（company-tearsheet / morning-note / initiating-coverage / earnings-analysis / comps-valuation / dcf-model-builder / event-scenario-analyzer / thesis-tracker），部分含 references 与质量清单 | 命中 `single-deep-report.md` 路由表的触发词时，加载对应 `SKILL.md` |
| `data-layer/` | 脚本 + 契约 | 统一数据层：接口契约、错误码容错表、四大数据源对照、取数纪律八条、AKShare 优先适配脚本、neodata 参考实现（`neodata-reference/`） | 所有模式取数统一走这里；见其 `README.md` |
| `md-to-html/` | 管线 | 圆桌/研报报告渲染：body 片段 → render.py 套壳（shell.html）→ 自动内嵌头像（base64）→ 单文件 HTML | `python3 md-to-html/scripts/render.py <body.html> <out.html> --title=... --date=...`；配套 `avatars/` 在 `investing-os/avatars/` |
| `distribution/` | 能力卡 | yanxu（公众号：建稿到草稿箱）+ agent-mail（邮箱：报告投递/订阅） | 需要分发时按卡内工具清单接入 |

## 依赖关系
- `research-deliverables/` 取数依赖 `data-layer/`；
- 全部模式卡的"报告变分享页"环节依赖 `md-to-html/`；
- `md-to-html` 默认头像路径（脚本相对 `../../../avatars/`）指向 `investing-os/avatars/`——**移动目录时请同步调整**。

## 归档说明
- 研股股其余 8 个低频技能与 5 份 MCP 工具文档 → `../../docs/归档/`；
- 原名包中的 westock / neodata 技能文档 → 能力已并入 `data-layer/README.md` 对照表，原始文档在 `../../docs/归档/`。

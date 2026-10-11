# 交易分析团队 · 移植指南

> 打包日期：2026-10-11 ｜ 来源：WorkBuddy 专家插件「交易分析团队 / Trading Analysis Team」（trading-agent）
> 用途：把"1 首席策略官 + 12 位专业角色、5 阶段对抗式流水线"的多智能体投研系统移植到你自己的工作台

---

## 一、包里有什么（21 个文件）

```
交易分析团队-移植包/
├── README-移植指南.md              ← 本文件
├── MCP-数据接入指南.md              ← 唯一数据源 neodata 的接入／替代方案
├── expert-package/                 ← 专家插件原样拷贝（纯 Markdown，可直接改）
│   ├── agents/                     ★ 核心资产：13 份智能体提示词（共 ~48KB）
│   │   ├── trading-team-lead.md          主理人「何执舟」·首席策略官（编排 SOP + 报告模板，19KB）
│   │   ├── market-analyst.md             「涂一线」·技术分析师（SMA/EMA/MACD/RSI/布林带/ATR）
│   │   ├── fundamentals-analyst.md       「季本实」·基本面分析师（财报/盈利/成长/估值）
│   │   ├── news-analyst.md               「闻一新」·新闻分析师（公告/政策/宏观/产业链）
│   │   ├── sentiment-analyst.md          「莫慌言」·情绪分析师（资金流/机构评级/龙虎榜/两融/北向）
│   │   ├── bull-researcher.md            「牛正阳」·多头研究员（增长/壁垒/信号共振/反驳空头）
│   │   ├── bear-researcher.md            「熊正寒」·空头研究员（下行风险/估值透支/逻辑证伪）
│   │   ├── research-manager.md           「蔡定锋」·研究主管（裁判多空辩论 → [投资计划]）
│   │   ├── trader.md                     「程交远」·交易员（FINAL TRANSACTION PROPOSAL + 价位）
│   │   ├── aggressive-risk-analyst.md    「甘为先」·激进风险分析师
│   │   ├── conservative-risk-analyst.md  「沈行远」·保守风险分析师
│   │   ├── neutral-risk-analyst.md       「钟允平」·中性风险分析师
│   │   └── risk-manager.md               「严控风」·风险主管（裁判三方风险 → [最终交易决策]）
│   ├── rules/trading-agent_rules.md      场景规则（触发条件 + 能力清单 + 并行纪律，6.9KB）
│   ├── skills/trading-analysis/SKILL.md  ★ 主协调器技能（阶段间输入输出契约 + Phase 5 报告模板，9.5KB）
│   └── .codebuddy-plugin/plugin.json     插件清单（13 agent 注册 + teamInfo + 成员中英文名映射）
└── data-source/
    └── neodata-financial-search/        ★ 本团队唯一数据源技能（SKILL.md + reference.md + 2 个取数脚本）
```

> 说明：`expert-package/` 是插件原样拷贝（未改动一个字节）；数据源技能单独放在 `data-source/`，方便你替换成自己的数据层。
> 插件清单里引用的 `avatars/*.png`（13 张头像）未随市场包落到本地，仅影响界面观感，不影响任何分析能力。

---

## 二、架构解析：五阶段"漏斗 + 对抗辩论"

与本系列其他包不同，这套系统的核心不是"多视角圆桌"，而是**先扩散再收敛、且在关键节点强制对抗**：

```
Phase 1  四维采集【并行】  market / fundamentals / news / sentiment ── 四人同时跑，互不可见
        ↓  4 份报告：技术面 / 基本面 / 新闻面 / 情绪面
Phase 2  多空辩论【顺序】  bull-researcher → bear-researcher → research-manager
        ↓  [多头论证] → [空头论证] → ★[投资计划]（必须给明确方向）
Phase 3  交易决策【单一】  trader
        ↓  ★[交易员决策]：FINAL TRANSACTION PROPOSAL + 入场/目标/止损价
Phase 4  风险评估【并行+顺序】
        4.1 三方风险辩论【并行】aggressive / conservative / neutral ── 三人同时跑
        ↓  3 份风险论证
        4.2 risk-manager 裁决【顺序】
        ↓  ★[最终交易决策]（风险调整后的 BUY/SELL/HOLD + 仓位）
Phase 5  汇编落盘【单一】  主理人 → Markdown 摘要 + 自包含 HTML 可视化报告
```

**决定产出质量的 5 条铁律**（移植时必须保留语义）：

1. **主理人不代写**——何执舟只做编排与汇编，技术分析/财报分析/多空论证/风险诊断/交易决策必须由对应角色输出后才采信
2. **该并行的必须并行**——Phase 1（4 人）与 Phase 4.1（3 人）立场独立、无数据依赖，顺序调用等于"后一个人偷看前一个人的答案"，多视角价值直接归零
3. **该顺序的必须顺序**——Phase 2 / Phase 3 / Phase 4.2 存在上下游依赖，输入必须完整传递（不是摘要，是原文）
4. **裁决不许和稀泥**——研究主管与风险主管必须给出明确 Buy/Sell/Hold；**Hold 不是默认项**，只在"存在明确的等待更好时机理由"时才成立
5. **每个角色有专属产物标记**（如 `[市场技术分析报告]`、`Bull Analyst: [多头论证]`、`FINAL TRANSACTION PROPOSAL`），阶段间靠标记精准引用——这是流水线的"接口协议"

---

## 三、三层架构（移植映射表）

| 层 | WorkBuddy 里的机制 | 对应文件 | 移植到你的工作台 |
|---|---|---|---|
| ① 人设层 | Expert 主提示词 + 12 个子代理提示词 | `agents/*.md`（13 份） | 主编排人 → Supervisor System Prompt；12 个角色 → 12 个 Worker Agent 的 System Prompt |
| ② 编排层 | Skill 按需加载 + 阶段间输入输出契约 | `skills/trading-analysis/SKILL.md`、`rules/*.md` | 编排图定义（节点/边/并发）或编排器 System Prompt |
| ③ 工具层 | MCP 连接器 / 取数技能 | `data-source/neodata-financial-search/` + `MCP-数据接入指南.md` | 配置 MCP Client 或换成你自己的数据层 |

**为什么分层很关键**：13 份提示词合计约 48KB，其中主理人一份就 19KB。若全部塞进单次 System Prompt，会严重稀释注意力。原设计里**主理人提示词常驻、成员提示词在 spawn 时才各自注入**——移植时保留这个"编排者常驻 + 成员按需注入"的模式，是成本与质量的最佳平衡点。

---

## 四、机制 → 通用框架原语映射

| 本系统机制 | 作用 | 映射到常见框架 |
|---|---|---|
| `trading-team-lead.md` | 编排：确认标的目标 → 拆阶段 → 调度 → 整合 | Supervisor / Orchestrator 节点的 System Prompt |
| 12 份角色提示词 | 各自人设 + 方法论 + 产物标记 | 12 个 Worker Agent 的 System Prompt（各自独立，互不共享） |
| `TeamCreate`（Phase 1 / 4.1） | 创建协作空间 + 并行拉起成员 | LangGraph `Send()` fan-out / CrewAI Crew / AutoGen GroupChat / `asyncio.gather` 并发 LLM 调用 |
| `SendMessage` 回传 | 成员把完整报告正文交回主理人 | Worker 返回值 / state 聚合（**正文即交付物**） |
| 阶段间原文传递 | Phase 2/3/4 的输入是上游**完整产出原文** | 图的有向边：fan-out → fan-in → 线性链 |
| 产物标记（`[投资计划]` 等） | 汇编层识别并结构化每份产出 | 结构化输出 schema / JSON 字段 / 命名消息类型 |
| 裁决节点（research-manager / risk-manager） | 强制收敛为单一决策 | 图上的 Decision 节点，输出枚举 BUY/SELL/HOLD |
| Phase 5 报告模板（摘要表 + 四维摘要 + 辩论结论 + 操作建议） | 固定产出骨架 | 主理人的输出模板（照抄即可） |
| HTML 可视化规范（雷达图/走势图/多空对比/风险三角，Chart.js） | 报告变高保真分享页 | 直接复用：自包含 HTML，零后端 |

**最小可行移植（不上多智能体框架）**——用 7 次 LLM 调用就能拿到约 80% 的价值：

```
第 1 组（4 次并发）：标的 + 数据快照 + 日期
   × 各自 agents/{market,fundamentals,news,sentiment}-analyst.md 作 System Prompt
第 2 组（3 次串行）：4 份报告原文 → bull → bear → research-manager
第 3 组（1 次）：[投资计划] + 4 份报告 → trader
第 4 组（3 次并发 + 1 次串行）：三个 risk 提示词并发 → risk-manager 汇总
第 5 组（1 次）：主理人提示词的"报告模板"章节 → 最终报告
```
丢掉工作流引擎的细节，只要**保住"并发不串行"和"原文传递"两条**，多视角对抗的增量就还在。

---

## 五、数据依赖：neodata-financial-search（本团队唯一数据源）

本团队硬性规定：**所有金融数据必须且只能**走 `neodata-financial-search`，禁止混用多数据源（避免口径不一致引发幻觉）。该技能是**自然语言**金融数据召回服务，覆盖股票（A股/港股/美股/英股/日股/韩股）、指数、板块、公募基金、债券、期货、期权、宏观、外汇、大宗商品十大类，外加研报/舆情/新闻/交易日历，共 130+ 数据工具。

移植到你的工作台有两条路线：

1. **有凭据路线**：按 `data-source/neodata-financial-search/scripts/query.py` 的请求结构（POST JSON，`query` + `channel=neodata` + `sub_channel=workbuddy` + `Bearer <凭证>`）直接对接，或向服务商申请独立凭据
2. **无凭据路线**：用 AKShare / Tushare / 东方财富 / 大智慧 / 腾讯自选股等替代，改写 SKILL.md 里的取数步骤即可——**13 份角色提示词的方​​法论不依赖具体数据源**，只依赖"能拿到行情/财务/资金/新闻"

> 详细字段、鉴权机制与替代清单见同目录 **`MCP-数据接入指南.md`**。

---

## 六、不可移植部分（明确告知）

| 资产 | 原因 | 替代方案 |
|---|---|---|
| WorkBuddy 平台系统指令与 TeamCreate/Agent/SendMessage 等运行机制 | 平台运行配置，不在交付范围 | 按第四节自己搭编排（LangGraph / CrewAI / AutoGen / 自研） |
| `connect_cloud_service` 鉴权通道 | 绑定 WorkBuddy 账号体系，换取短时凭证走代理端点 | 向数据服务商申请独立凭据，或换开源数据源 |
| `avatars/*.png`（13 张成员头像） | 市场包注入，未落本地 | 可自绘或忽略，不影响能力 |
| 底层模型能力 | 平台托管 | 接入你选定的任意大模型 API（注意：需要支持长 System Prompt） |

---

## 七、落地清单（建议顺序）

1. **先单测角色**：任取 3 份角色提示词（建议组合 `market-analyst` / `bull-researcher` / `conservative-risk-analyst`，立场差异最大），各跑一次"分析某只股票"，确认输出真的长在各自的独特增量区，而不是同质化
2. **再搭 Phase 1 并发**：实现"4 次并发 + 结果收集"，检查每份产出是否带上了正确的产物标记（标记错位会让下游全乱）
3. **串起 Phase 2 辩论**：4 份报告原文 → bull → bear → research-manager，验证研究主管**确实给出了明确方向**而不是"双方都有道理"
4. **补 Phase 3 / 4**：trader 必须输出 `FINAL TRANSACTION PROPOSAL`；三方风险评估并发后交 risk-manager 裁决，检查它是否在 **Hold 的适用条件**上守住了纪律
5. **最后接数据层**：从一家数据源起步，把各角色提示词里的"数据获取"段落映射到真实工具调用；保留数据来源标注与"低置信度标注"习惯
6. **保留合规底线**：报告末尾的免责声明、"不编造数字"、数据来源可追溯、"不构成投资建议"——这几条建议**原样保留**，这是投资类产品的合规底线

---

## 八、与同系列其他移植包的关系

| 包 | 形态 | 适合场景 |
|---|---|---|
| `研股股-专家移植包` | 单专家深度报告 | "给我一份某只票的深度研究报告" |
| `投研专家团-移植包` | 星型圆桌（6 视角并行，扁平） | "多人各抒己见，分歧本身就是产出" |
| `投资大师专家团-移植包` | 四阶段流水线（19 大师 → 风险官 → 组合经理） | "用经典投资流派框架做多视角筛选" |
| **本包（交易分析团队）** | 五阶段漏斗 + **两轮强制对抗辩论** | "要一个敢下结论的 BUY/SELL/HOLD，且必须经得起多空与风险三方质疑" |

**本包的独特增量**：它是四者中**唯一内置"辩论 + 裁决"决策收敛机制**的——先让多空互相攻击、再让激进/保守/中性三方互相攻击，两次对抗后才落决策，专门治"分析一堆、结论含糊"。

---

*13 份提示词均为纯 Markdown 文本，可自由裁剪。建议保留文件头部的 `name` / `description` frontmatter，便于任何支持 agent/skill 路由的框架解析；建议保留每位角色的"独特增量区"定义与产物标记——这是流水线能跑通的接口协议。*

# 投资大师专家团 · 移植指南

> 打包日期：2026-10-11 ｜ 来源：WorkBuddy 专家插件「投资大师专家团 / AI Hedge Fund」（investment-masters-team）
> 用途：把"1 基金经理 + 19 位投资大师/分析师 + 风险官 + 组合经理"的**四阶段流水线多智能体投研系统**移植到你自己的工作台

---

## 一、包里有什么（51 个文件，6.2MB）

```
投资大师专家团-移植包/
├── README-移植指南.md          ← 本文件
├── MCP-数据接入指南.md          ← 唯一数据源 neodata 的接入/替代方案
└── expert-package/             ← 完整专家插件（原样拷贝，纯 Markdown，可直接改）
    ├── agents/                 ★ 核心资产：22 份智能体提示词
    │   ├── hedge-fund-lead.md            主理人「贺知衡」·基金经理（编排 SOP，20KB）
    │   ├── oracle-of-omaha.md            奥马哈先知（价值 / 护城河 / Owner Earnings DCF）
    │   ├── charlie-munger.md             芒格（ROIC 一致性 / 可预测性 / FCF 倍数）
    │   ├── magellan-captain.md           麦哲伦舵手（GARP / PEG / 十倍股）
    │   ├── the-big-short.md              大空头（深度价值逆向 / EV-EBIT / 资产负债表）
    │   ├── black-swan-prophet.md         黑天鹅之父（反脆弱 / 尾部风险 / 凸性）
    │   ├── mama-wood.md                  木头姐（颠覆性创新 / 大 TAM / 研发强度）
    │   ├── ben-graham.md                 格雷厄姆（格雷厄姆数字 / NCAV 净净值）
    │   ├── wall-street-activist.md       华尔街斗牛士（品牌护城河 / 资本纪律 / 催化剂）
    │   ├── macro-king.md                 宏观之王（非对称风险收益 / 动量 / 资本保全）
    │   ├── dhandho-master.md             Dhandho 掌门（下行保护 / FCF 收益率 / 翻倍潜力）
    │   ├── phil-fisher.md                费雪（研发创新 / 管理层质量 / 利润率一致性）
    │   ├── dean-of-valuation.md          估值教父「葛衡量」（FCFF DCF / WACC / 情景分析）
    │   ├── rakesh-jhunjhunwala.md        金君瓦拉（新兴市场成长 / 安全边际 >30%）
    │   ├── fundamentals-analyst.md       基本面分析师「季本实」
    │   ├── technicals-analyst.md         技术面分析师「涂一线」
    │   ├── valuation-analyst.md          估值分析师「谷衡值」
    │   ├── sentiment-analyst.md          情绪分析师「莫慌言」
    │   ├── growth-analyst.md             成长分析师「成长青」
    │   ├── news-sentiment-analyst.md     新闻情绪分析师「闻风声」
    │   ├── risk-manager.md               ★ 风险管理师「严控风」（Phase 2）
    │   └── portfolio-manager.md          ★ 投资组合经理「裴持衡」（Phase 3，出 BUY/SELL/HOLD）
    ├── skills/
    │   └── neodata-financial-search/     ★ 唯一数据技能（SKILL.md + reference.md + 2 个取数脚本）
    ├── .codebuddy-plugin/plugin.json     插件清单（22 agent 注册 + teamInfo + 头像映射）
    ├── avatars/                          23 张成员头像 PNG（HTML 报告渲染用）
    └── .downloaded_at                    下载时间戳
```

---

## 二、架构解析：这是一条"四阶段流水线"，不是简单圆桌

与「投研专家团」的星型并行不同，本系统是**漏斗式流水线**——19 路独立信号先并行采集，再逐级收敛为一份决策：

```
Phase 0  询问席位   ── 先用多选组件问用户"这次请哪几位大师"，按勾选子集启动
        ↓
Phase 1  并行采集   ── 选中的 N 位大师/分析师同时跑（各自取数 → 各自框架分析 → 各出一份[x分析信号]）
        ↓  N 份信号
Phase 2  风险约束   ── risk-manager 收齐 N 份信号，算波动率 / 仓位上限 / 风险等级
        ↓  1 份[风险评估报告]
Phase 3  组合决策   ── portfolio-manager 基于 N 份信号 + 风险报告，给出明确 BUY / SELL / HOLD
        ↓  1 份[最终投资决策]
Phase 4  汇编落盘   ── 主理人整合成结构化报告，写入 deliverables/
```

**决定产出质量的 5 条铁律**（移植时必须保留语义）：

1. **主理人不代写**——贺知衡只做编排与汇编，任何专业结论必须由对应成员输出后才采信
2. **Phase 1 必须并行**——19 位互不可见，信号独立才有多视角价值；顺序调用等于偷看答案
3. **风险/组合席位固定参与**——无论用户勾选谁，Phase 2、3 永远执行（决定必出 BUY/SELL/HOLD，不许"分歧大"就默认 HOLD）
4. **信息经主理人中转**——成员之间不直连，跨成员信息流只在汇编层汇合
5. **信号聚合投票**——最终报告必须给出"看多 X / 看空 Y / 中性 Z"的显式统计，分歧本身是产品的一部分

---

## 三、三层架构（移植映射表）

| 层 | WorkBuddy 里的机制 | 对应文件 | 移植到你的工作台 |
|---|---|---|---|
| ① 人设层 | Expert 主提示词 + 子代理提示词 | `agents/*.md`（22 份） | 主编排人 → Supervisor System Prompt；20 个成员 → 20 个 Worker Agent 的 System Prompt |
| ② 技能层 | Skill 按需加载 | `skills/neodata-financial-search/` | 数据层知识包 / 取数工具封装 |
| ③ 工具层 | MCP 连接器 | `MCP-数据接入指南.md` + 脚本 | 配置 MCP Client 或换等价数据源 |

**为什么分层很关键**：22 份提示词合计约 60KB，其中主理人一份就 20KB。若全部塞进单次 System Prompt，会严重稀释注意力。原设计里主理人提示词承载"席位表 + 任务模板 + SOP + 报告模板"，成员提示词在 spawn 时才各自注入——**移植时保留这个"编排者常驻、成员按需注入"的模式**。

---

## 四、移植映射表（机制 → 通用框架原语）

| 本系统机制 | 作用 | 映射到常见框架 |
|---|---|---|
| 主理人提示词 `hedge-fund-lead.md` | 席位选择、维度派发、SOP 编排、报告模板 | Supervisor / Orchestrator 节点 System Prompt |
| 20 份成员提示词 | 各自的人设 + 方法论 + 产物标记 | 20 个 Worker Agent System Prompt（每人一份，互不共享） |
| `AskUserQuestion` 多选 | Phase 0 让用户勾选参与席位 | 前端多选框 / 配置项；或直接固定席位集 |
| `TeamCreate` + `Agent` spawn | 建协作空间 + Phase 1 并行拉起 | LangGraph `Send()` 并发 / CrewAI Crew / AutoGen GroupChat / `asyncio.gather` 多发 LLM 调用 |
| `SendMessage` 回传信号 | 成员把 `[xx分析信号]` 交回主理人 | Worker 返回值 / state 聚合 |
| 阶段间顺序依赖 | Phase1→2→3 严格串行 | 图的边：fan-out 后 fan-in 到 risk 节点，再到 portfolio 节点 |
| 产物标记（如 `[巴菲特分析信号]`） | 汇编层识别并结构化每份产出 | 结构化输出 schema / JSON 字段 |
| 落盘规范 `deliverables/investment-masters/` | 报告存盘命名 | 按你项目的产物目录改 |

**最小可行移植（不上多智能体框架）**：把 Phase 1 做成 **N 次并发 LLM 调用**——同一个"标的 + 数据快照 + 日期"、各自 agents/*.md 作 System Prompt，收集 N 份信号后，串行喂给 risk-manager、再喂给 portfolio-manager 提示词，最后用主理人提示词的"报告模板"章节汇编。丢掉编排细节也能拿到约 80% 的多视角价值。

---

## 五、数据依赖：neodata-financial-search（本团队唯一数据源）

本团队规定：**所有金融数据必须且只能**走 `neodata-financial-search`，禁止混用多数据源（避免口径不一致引发幻觉）。该技能是自然语言金融数据召回服务，覆盖 A股/港股/美股/日股/韩股 + 指数/板块/基金/宏观/外汇/大宗商品 七大类。

移植到你的工作台有两条路线：

1. **有凭据路线**：向数据服务商（腾讯 NeoData）申请独立 API 凭据，按 `scripts/query.py` 的请求结构（`query` / `channel=neodata` / `sub_channel` + Bearer 鉴权）直接对接
2. **无凭据路线**：用 AKShare / Tushare / 东方财富 / 大智慧 / 腾讯自选股等替代，改写 `SKILL.md` 里的调用步骤即可——**20 份成员提示词的方法论不依赖具体数据源**，只依赖"能拿到行情/财务/资金/新闻"

> 详细接入字段、鉴权机制与替代清单见同目录 **`MCP-数据接入指南.md`**。

---

## 六、不可移植部分（明确告知）

| 资产 | 原因 | 替代方案 |
|---|---|---|
| WorkBuddy 平台系统指令与团队编排逻辑 | 平台运行配置，不在交付范围 | 按第四节自己搭编排（LangGraph / CrewAI 等） |
| `connect_cloud_service` 鉴权通道 | 绑定 WorkBuddy 账号体系，取 `tempToken` 后走代理端点 | 向数据服务商申请独立凭据，或换开源数据源 |
| 底层模型能力 | 平台托管 | 接入你选定的任意大模型 API |
| 头像 PNG | 仅影响渲染观感 | 可保留，可替换 |

---

## 七、落地清单（建议顺序）

1. **先单测成员**：任取 3 份成员提示词（建议奥马哈先知 / 木头姐 / 黑天鹅之父，风格差异最大），各跑一次"分析某只股票"，确认输出真的长在各自的独特增量区，而非同质化
2. **再搭 Phase 1**：实现"N 次并发 + 结果收集"，跑通"多视角分析"场景，检查每份产出是否带上了对应的产物标记
3. **串起 Phase 2/3**：把 N 份信号喂给风险官提示词，再把"信号 + 风险报告"喂给组合经理提示词，验证决策节点确实输出明确的 BUY/SELL/HOLD
4. **最后接数据层**：从一家数据源起步，把成员提示词里的"数据获取"步骤映射到真实工具调用；保留数据来源标注
5. **保留合规底线**：报告末尾的免责声明、"不编造数字"、数据来源可追溯这几条建议原样保留

---

*22 份提示词均为纯 Markdown 文本，可自由改裁。建议保留文件头部的 `name` / `description` 元数据格式，便于任何支持 skill/agent 路由的框架解析。*

> 系列关系：本包（多大师流水线）与同系列 `研股股-专家移植包`（单专家深度报告）、`投研专家团-移植包`（多视角圆桌）三者互补，可按场景取用。

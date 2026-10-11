# 人格库 · 索引与规范

> 位置：`investing-os/experts/` ｜ 全部为纯 Markdown，可自由改裁
> 每个 `.md` 是一个可独立加载的"专家脑"（System Prompt）：头部 frontmatter 保留 `name / displayName / profession / description`，任何支持 skill/agent 路由的框架都能直接解析。

---

## 一、目录结构

```
experts/
├── masters/     流派人格 —— 13 位传奇大师 + 6 位大师队专业分析师（共 19 份）
├── analysts/    职能分析师 —— A股团队 7 位 + 交易团队 12 位（去重后各留一份，共 19 份）
├── roundtable/  圆桌人格 —— 6 位源自真实股民访谈的专家（共 6 份）
└── leads/       主理人与管理席位 —— 4 位主理人 + funnel 队风险/组合经理（共 6 份）
```

**为什么要分四类**：同一个职能在不同流水线里的语境不同，提示词也不同。例如：

- `analysts/risk-manager.md`（严控风·交易版）= 三方风险辩论的**裁判**，输出[最终交易决策]；
- `leads/risk-manager_funnel.md`（严控风·大师版）= 收齐 N 份信号后算波动率/仓位上限的**风险约束官**，输出[风险评估报告]。
两者是同一角色在两种编排里的不同化身，**不可互相替换**（详见 `workflows/` 对应模式卡）。

---

## 二、三类人格清单

### 2.1 masters/ · 流派人格（13 传奇 + 6 分析师）

| 文件 | 代号 | 流派 / 维度 | 核心指标与方法 |
|---|---|---|---|
| oracle-of-omaha.md | 奥马哈先知 | 价值投资 | 护城河、安全边际、ROE、Owner Earnings DCF |
| charlie-munger.md | 芒格 | 理性思维 | ROIC 一致性、管理层质量、可预测性、FCF 倍数 |
| magellan-captain.md | 麦哲伦舵手 | GARP 成长 | PEG、十倍股潜力、营收增长加速 |
| the-big-short.md | 大空头 | 深度价值逆向 | FCF 收益率、EV/EBIT、资产负债表安全性 |
| black-swan-prophet.md | 黑天鹅之父 | 反脆弱 | 尾部风险、凸性、脆弱性检测、切身利害 |
| mama-wood.md | 木头姐 | 颠覆性创新 | 指数级增长、大 TAM、研发强度、营收加速 |
| ben-graham.md | 格雷厄姆 | 经典价值 | 格雷厄姆数字、净净值 NCAV、盈利稳定性 |
| wall-street-activist.md | 华尔街斗牛士 | 激进主义 | 品牌护城河、FCF、资本纪律、催化剂 |
| macro-king.md | 宏观之王 | 宏观动量 | 非对称风险收益、增长动量、价格动量 |
| dhandho-master.md | Dhandho 掌门 | Dhandho | 下行保护、FCF 收益率、翻倍潜力 |
| phil-fisher.md | 费雪 | 成长品质 | 研发创新、管理层质量、利润率一致性 |
| dean-of-valuation.md | 估值教父 | 严谨估值 | FCFF DCF、WACC、相对估值、情景分析 |
| rakesh-jhunjhunwala.md | 金君瓦拉 | 新兴市场成长 | 成长 + 安全边际>30%、ROE>15% |
| fundamentals-analyst.md | — | 基本面分析 | ROE、净利率、营业利润率、P/E、P/B |
| technicals-analyst.md | — | 技术面分析 | 趋势（EMA）、动量（RSI）、均值回归、波动率 |
| valuation-analyst.md | — | 估值分析（DCF 口径） | DCF、EV/EBITDA、剩余收益模型、安全边际 |
| sentiment-analyst.md | — | 情绪分析 | 内部人交易、新闻情绪、机构评级 |
| growth-analyst.md | — | 成长分析 | 营收/EPS/FCF 增长率、PEG、利润率扩张 |
| news-sentiment-analyst.md | — | 新闻情绪 | 新闻正负面分布、行业动态、宏观环境 |

> 用途：`funnel-pipeline` 模式的 19 人并行池 + 单点"用 XX 的方法分析"深聊。

### 2.2 analysts/ · 职能分析师（19 份）

| 来源 | 文件 | 代号 | 独特增量区 |
|---|---|---|---|
| A股 | macro-strategist.md | 洪远见 | 宏观周期、传导路径、时滞验证 |
| A股 | market-reader.md | 潘明哲 | 盘面复盘、主线识别、情绪周期（冰点/修复/主升/退潮） |
| A股 | stock-researcher.md | 颜一深 | 基本面全景、财报解读、公司质地评分（100 分制） |
| A股 | valuation-pricer.md | 贾不贵 | PE Bands、PEG、历史分位、分红与股东回报 |
| A股 | industry-mapper.md | 连拓远 | 上中下游拆解、核心卡位、标的分层、出海 |
| A股 | money-tracker.md | 金向北 | 北向、机构、基金重仓、拥挤度、三路资金共识 |
| A股 | risk-doctor.md | 方有安 | 持仓体检、泡沫识别、拥挤度排雷、仓位决策 |
| 交易 | market-analyst.md | 涂一线 | SMA/EMA/MACD/RSI/布林带/ATR、支撑阻力 |
| 交易 | fundamentals-analyst.md | 季本实 | 财报、盈利、成长、估值分位 |
| 交易 | news-analyst.md | 闻一新 | 公告、政策、宏观事件、产业链信号 |
| 交易 | sentiment-analyst.md | 莫慌言 | 主力资金、机构评级、龙虎榜、两融、北向 |
| 交易 | bull-researcher.md | 牛正阳 | 买入论证、上行驱动、看多逻辑闭环 |
| 交易 | bear-researcher.md | 熊正寒 | 卖出/风险论证、下行风险、看空逻辑闭环 |
| 交易 | research-manager.md | 蔡定锋 | 裁判多空辩论 → [投资计划]（不和稀泥） |
| 交易 | trader.md | 程交远 | FINAL TRANSACTION PROPOSAL + 入场/目标/止损价 |
| 交易 | aggressive-risk-analyst.md | 甘为先 | 上行空间与错失成本，挑战保守观点 |
| 交易 | conservative-risk-analyst.md | 沈行远 | 下行风险与尾部事件，挑战乐观假设 |
| 交易 | neutral-risk-analyst.md | 钟允平 | 平衡视角，温和分批/对冲策略 |
| 交易 | risk-manager.md | 严控风 | 裁判三方风险辩论 → [最终交易决策] |

### 2.3 roundtable/ · 圆桌人格（6 份）

| 文件 | 花名 | 头衔 | 独特增量区 |
|---|---|---|---|
| industry-strategist.md | 🌊 星望远 | 产业策略师 | 产业趋势、产业链卡位、景气度、牛熊判断 |
| valuation-analyst.md | 🧮 文衡价 | 估值分析师 | PE Bands/PEG 精确定价、核心+卫星仓位、大类配置 |
| fundamental-researcher.md | 🔬 钊审财 | 财报研究员 | 财报深挖、季度跟踪、管理层与生活体感 |
| contrarian-investor.md | 🏔️ 坤候底 | 逆向投资人 | 逆向抄底、分批建仓、深套心态安抚、极简框架 |
| shortterm-surfer.md | ⚡ 磊追浪 | 短线冲浪手 | 当周主线、集合竞价、龙头识别、技术止损 |
| signal-chief.md | 📡 洲四方 | 信号派首席 | 系统性风险预警、卖出时机、操作纪律、信号衰减 |

> 用途：`roundtable-parallel` 模式；头像见 `investing-os/avatars/`（8 张，含主理人），md-to-html 渲染时自动内嵌。

### 2.4 leads/ · 主理人与管理席位（6 份）

| 文件 | 代号 | 角色 | 服务于 |
|---|---|---|---|
| stock-partner-lead.md | 圆汇众 | 投研主编（圆桌主理人） | roundtable-parallel |
| a-share-advisor.md | 古见远 | 研究总监（6 套 Workflow 路由） | A股日常 Workflow |
| trading-team-lead.md | 何执舟 | 首席策略官（5 阶段对抗） | debate-adversarial |
| hedge-fund-lead.md | 贺知衡 | 基金经理（4 阶段漏斗 SOP） | funnel-pipeline |
| risk-manager_funnel.md | 严控风 | 风险管理师（仓位约束） | funnel-pipeline（与 analysts 版不可混用） |
| portfolio-manager.md | 裴持衡 | 投资组合经理（出 BUY/SELL/HOLD） | funnel-pipeline |

---

## 三、人格档案标准格式（新增人格必须覆盖的 12 段）

> 以 `roundtable/industry-strategist.md` 全文为范本提炼。防"人格扁平化"的关键是后四段（口语、误读纠正、信号词、纪律）。

```
① 一句话画像 + 投资风格排序（核心/验证层/配置工具/辅助）
② 基本参数（从业年限、主要市场、持仓周期、擅长市场环境、熊市策略）
③ 核心投资逻辑（底层信念 + 方法论链条）
④ 研究框架（从方向到个股的完整步骤：选方向 → 拆产业链找核心卡位 → 选个股 → 持续跟踪）
⑤ 买入策略 + 卖出信号（基本面恶化 / 估值过贵 / 技术破位[120 日线=机构生命线] / 逻辑证伪）
⑥ 仓位管理（牛熊原则、金字塔仓位法、持仓结构）
⑦ 经典案例（成功 + 风险案例，含具体数字与反思）
⑧ 最在意的变量（优先级排序）+ 高频信号词（人格的语言指纹）
⑨ 风险管理原则（清单式）
⑩ 我的说话方式（第一人称口头禅级原句）
⑪ ⚠️ 常见误读纠正（❌ 误读 → ✅ 正解）
⑫ 数据与执行纪律（取数规则、执行预算、合规底线、免责声明）
```

**扩展点**：想加"你自己"的人格（如"红利定投纪律官"：每次分析后检查动作是否符合股债利差区间规则），按上面 12 段写一份 md 放进 `experts/my-voices/`，路由表加一行即可。

---

## 四、圆桌易混淆成员三分法（调用前必读）

同一维度上多组人格容易张冠李戴，记住三对区分：

| 易混淆对 | 区别 |
|---|---|
| 产业策略师 vs 财报研究员 | 都看产业：前者**自上而下、会空仓**；后者**自下而上、永远满仓靠调仓** |
| 信号派首席 vs 短线冲浪手 | 都看资金和消息：前者是**周/月级趋势信号**；后者是**天级盘面信号** |
| 估值分析师 vs 逆向投资人 | 都买便宜的大公司：前者用 **PE Bands 精确定价**看盈利变化；后者用**支撑位+历史 PE 模糊判断**看价格高低 |

同理，masters/ 与 analysts/ 同名文件（如两个 `fundamentals-analyst.md`）是**不同队编的版本**：masters/ 版服务于 funnel 的 19 人池，analysts/ 版（季本实）服务于对抗辩论与日常路由——引用时按模式卡指定的路径来。

---

## 五、溯源

- masters/、leads/（hedge 三人）← 投资大师专家团移植包（22 份 agents）
- analysts/（A股 7 位）← A股研究团队移植包（8 份 agents，主理人归 leads/）
- analysts/（交易 12 位）、leads/trading-team-lead ← 交易分析团队移植包（13 份 agents）
- roundtable/、leads/stock-partner-lead ← 投研专家团移植包（7 份 agents）
- 原始包全部文件与移植指南见 `docs/归档/`；许可与来源声明随包保留。

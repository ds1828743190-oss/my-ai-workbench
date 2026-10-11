# 统一数据层 · data-layer

> 四份原包 MCP/数据指南收敛为一套。所有模式（圆桌/漏斗/对抗/日常）取数统一走本层。
> 上层纪律：数字必标来源与日期；取不到就标注降级，**绝不编造**。

---

## 一、统一接口契约（对齐 neodata `query.py`，作为本层标准封装）

```
POST {endpoint}                                   # 默认主推：本地 AKShare 适配（见下）
Header: Authorization: Bearer <凭证>              # 连接器路线时使用；本地开源路线无需凭证
Body:   { "query": "自然语言问题", "channel": "neodata", "sub_channel": "workbuddy" }
可选:   data_type = all（默认推荐）/ api / doc
        ⚠️ 纪律：不要为"减小返回体积"默认加 api——实测会让 20-40% 本可由文章召回兜底的 query 变空结果
响应:   data.apiData（结构化：entity + apiRecall）/ data.docData（文档：docRecall）
        成功时 code="200"、suc=true
脚本:   neodata-reference/query.py（Python 3.7+）/ neodata-reference/query.sh（curl 封装）
凭证:   --token 参数 > 本地缓存 .neodata_token（12 小时有效）；缓存文件必须加入 .gitignore
```

## 二、错误码容错表（对接任何数据源都按此设计）

| code | 含义 | 处理 |
|---|---|---|
| `1001` | 未命中意图 | 改写 query，更具体 |
| `1616039101` | 参数值不合法 | 检查入参 |
| `1006` | 查询解析拒答 | 策略拦截/不支持场景，换问题 |
| HTTP 401/403 或 `40101` | 凭证失效 | 重取一次凭证；两次失败即判服务不可用，**停止重试** |

## 三、四大数据源能力对照

### 3.1 neodata（NeoData）——估值与利率主源｜自然语言召回，130+ 工具
- **十大类**：股票（A股/港股/美股/英股/日股/韩股：行情、盘口、财报三表、复合指标、资金流、股东、分红回购、龙虎榜、两融、大宗、业绩纪要）/ 指数（成分权重、估值百分位、盈利预测）/ 板块 / 公募基金（含 REITs）/ 债券（收益率曲线、信用评级）/ 期货 / 期权（希腊字母）/ 宏观（GDP/CPI/PMI/M2/社融/事件日历）/ 外汇 / 大宗商品；
- **辅助**：研报评级/目标价、盈利预测、舆情、财经快讯、交易日历；
- **约 90 个结构化工具**：`quote_and_kline`、`income_statement`、`balance_sheet`、`cash_flow`、`valuation`、`fund_holdings`、`margin`、`connect_stats`、`sector_flow_rank`、`macro_cn`、`yield_curve`、`index_valuation`、`supply_chain`、`ratings`、`news` 等；
- **历史纵深**：A股 1990 / 港股 1980 / 美股 1950 起。参考实现见 `neodata-reference/`。

### 3.2 westock-mcp（腾讯自选股）——行情主源 + 选股引擎
- `data_*`：kline / quote / finance / fund_flow / lhb / north_holding / chip / hot / report / dividend / shareholder / notice / technical / rating / search / consensus / news；
- `tool_*`：filter / strategy / ranking / label（条件/策略/标签/排行选股）；
- `portfolio_*`：paper_trade（模拟交易）/ watchlist（自选管理）；
- 返回格式 `{ok, data, message}`，`ok:false` 时**原样转述 message，禁止编造**；
- 代码格式：`sh600519` / `sz000001` / `hk00700` / `usAAPL`；板块 `pt01801080`。

### 3.3 dzh-mcp（大智慧）——个股级备用｜约 90 工具
- `getStockFinanceData`（财务）/ `findStockCodesBy*`（40+ 多维选股器）/ `getQuoteKline`（K线）/ F10 资料系列 / 板块、股东、分红送转、龙虎榜、大宗、研报公告、新闻舆情；
- ⚠️ **指数级 PE 字段口径异常（返回约 35 倍），永久禁用**——实盘验证过的规则，全项目继承。

### 3.4 开源替代（无凭据路线，零成本起步）——本项目默认
| 原能力 | 开源替代 |
|---|---|
| A股/港股/美股行情、财报、资金流 | **AKShare**（覆盖面最广，免费，默认主推） |
| A股财务、行情、指数 | Tushare（需积分） |
| 板块/资金/龙虎榜/两融/大宗 | 东方财富公开接口 |
| 美股行情/财报 | yfinance；历史长周期 K 线：AKShare / yfinance / Stooq |
| 兜底（连接器全挂） | 本地 a-stock-data 技能（腾讯直连 `qt.gtimg.cn`；⚠️ 指数必须显式传市场前缀，沪深300=`sh000300`） |

**快速起步**：`python3 akshare_adapter.py --selftest`（缺 akshare 时按提示安装：`pip install akshare -i https://pypi.tuna.tsinghua.edu.cn/simple`）。

## 四、取数纪律八条（全模式继承）

1. **换源整体替换，不混用**——口径不一致会引发幻觉；确需交叉印证时，每项数字标注来源。**唯一例外**：投资台核心策略流程继续执行 `workbenches/investment/strategy/数据源交叉印证协议.md` 的"两源一致才有效"更高标准；
2. **技术指标自算**——SMA/EMA/MACD/RSI/布林带/ATR 由分析师基于返回的日线数据自行计算（数据服务不直接给指标）；
3. **共享快照**——同一标的只取一次，注入所有成员任务说明，防重复取数；
4. **工具不是越多越好**——90+ 工具全挂会挤占上下文、降低路由准确率；按 Workflow 裁剪 6~10 个；
5. **工具文档即提示词**——references 里的参数与适用场景说明，直接作为"工具选择提示"注入；
6. **诚实降级**——数据通道不可用时降级联网搜索/其他源，产出中标注"待核实"与「降级取数」，**禁止编造**；交付时必须再次提醒精度受限；
7. **历史归历史，实时归实时**——档案里的价格是快照，只用于历史叙述；讨论"当前"必须重新查实时数据；
8. **数据来源可追溯**——引用必须标注具体来源（如 `data_quote 腾讯`、`WebSearch："…"`、`AKShare: stock_zh_index_daily`），禁止"综合来看""据了解"等无来源表述。

## 五、文件清单

| 文件 | 作用 |
|---|---|
| `README.md` | 本文件（契约 + 对照表 + 纪律） |
| `akshare_adapter.py` | 开源路线适配脚本（AKShare 优先；含 --selftest 自检） |
| `neodata-reference/SKILL.md`、`reference.md` | neodata 原始技能文档（接口契约参考） |
| `neodata-reference/scripts/query.py`、`query.sh` | neodata 取数脚本（请求/响应结构参考；凭证机制见 §一） |

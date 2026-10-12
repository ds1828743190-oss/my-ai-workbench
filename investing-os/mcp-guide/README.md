# MCP 接入与工具调用指南

> 本项目 Skill 层的数据与分发能力通过 **MCP（Model Context Protocol）** 接入外部服务。
> 本指南 = 接入方法（怎么配）+ 调用规范（怎么用）+ 降级路线（连不上怎么办）。

---

## 一、MCP 是什么

MCP 是开放标准：AI 客户端通过统一协议连接外部工具与数据服务。**只要环境支持 MCP Client，就能接入任何 MCP Server**——这是本项目跨平台复用的底层原因。

```
AI 客户端（WorkBuddy / Claude Code / Cursor / 自研）
   │  MCP 协议
   ├── 数据类 Server：neodata · westock · dzh
   ├── 分发类 Server：yanxu（公众号）· agent-mail（邮箱）
   └── 本地兜底：AKShare 脚本（非 MCP，纯本地）
```

## 二、配置格式（各客户端通用）

**本地进程式（stdio）**——适合本地命令行服务：
```json
{
  "mcpServers": {
    "my-finance-tool": {
      "command": "npx",
      "args": ["-y", "@some-org/some-mcp-server@latest"],
      "env": { "API_KEY": "<你的凭据>" }
    }
  }
}
```

**远程服务式（HTTP/SSE）**——适合云端 API：
```json
{
  "mcpServers": {
    "remote-data": {
      "url": "https://api.example.com/mcp",
      "headers": { "Authorization": "Bearer <你的凭据>" }
    }
  }
}
```

配置文件位置：Claude Desktop → `claude_desktop_config.json`；Cursor → `.cursor/mcp.json`；Claude Code → `~/.claude/` 下对应配置；自研 → 由 Client 代码读取。完整示例见 `configs/mcp-config.example.json`。

## 三、本项目协作的连接器清单

| # | 连接器 | 能力 | 核心工具 | 适用环节 |
|---|---|---|---|---|
| 1 | **neodata**（NeoData） | 自然语言金融数据召回，130+ 工具；股票（A/港/美/英/日/韩）、指数、板块、基金、债券、期货、期权、宏观、外汇、大宗 | `quote_and_kline`、`income_statement`、`valuation`、`index_valuation`、`yield_curve`、`macro_cn`、`ratings`、`news` 等 | 研究主源：估值/利率/长历史数据 |
| 2 | **westock-mcp**（腾讯自选股） | 行情与资讯、条件/策略/事件选股、模拟交易 | `data_*`（kline/quote/finance/fund_flow/lhb/north_holding/consensus…）、`tool_*`（filter/strategy/ranking/label）、`portfolio_*` | 行情主源 + 选股引擎 |
| 3 | **dzh-mcp**（大智慧） | 行情K线、财务三表、40+ 多维选股器、F10、龙虎榜、研报舆情 | `getStockFinanceData`、`findStockCodesBy*`、`getQuoteKline`、`getF10*` | 个股级备用源（**指数级 PE 字段口径异常，永久禁用**） |
| 4 | **yanxu**（言序） | 微信公众号建稿与发布：`list_wechat_accounts` / `list_theme_styles` / `create_article` / `publish_article`（止步草稿箱） | 同左 | 报告分发（自媒体台/晨报） |
| 5 | **agent-mail** | Agent 邮箱：`SendMessage` / `ListMessages` / `SearchMessages` / `ForwardMessage` / `ListAttachments` | 同左 | 报告定时投递、订阅研报接收 |

> 授权说明：各连接器授权绑定你当前平台的账号；**搬到其他环境需向对应服务商获取独立凭据**，或走 §五 开源路线。

## 四、工具调用规范（写进任何使用这些工具的提示词）

1. **返回格式**：westock 系返回 `{ok, data, message}`——`ok:false` 时**原样转述 message，禁止编造**；neodata 系成功时 `code="200"、suc=true`，数据在 `data.apiData` / `data.docData`；
2. **代码格式**：`sh600519`（沪）/ `sz000001`（深）/ `hk00700`（港）/ `usAAPL`（美）；板块 `pt01801080`；**指数必须显式传市场前缀**（沪深300=`sh000300`）；
3. **工具按需裁剪**：90+ 工具全挂会挤占上下文、降低路由准确率——单次任务挂 6~10 个相关工具；
4. **工具文档即提示词**：工具说明文档（字段表、场景指南）直接作为"工具选择提示"注入；
5. **共享快照**：同一标的只取一次行情快照，注入后续全部环节，防重复取数；
6. **错误处理**：鉴权失效（HTTP 401/403/40101）→ 重取一次凭证；两次失败即判服务不可用，**停止重试**并降级；参数类错误按接口说明修正；
7. **查询技巧**：数据类查询越具体越好（"XX 近6个月日线 开高低收量"优于"XX 数据"）；neodata 的 `data_type` 不要默认加 `api`（会让部分查询变空结果）。

## 五、数据源纪律与降级链

```
优先级：已授权连接器（neodata / westock / dzh）
   ↓ 不可用时
本地脚本：../skills/data-layer/akshare_adapter.py（AKShare 优先，含指数行情/官方PE/10Y国债/ETF双源）
   ↓ 仍不可用
联网搜索（仅补充非结构化资讯；关键数值标注来源与日期）
```

- **同一分析流程内单源不混用**（口径不一致会引发幻觉）；换源=整体替换并标注"降级取数"；
- 交叉印证仅限明确要求时（如个人策略流程的"两源一致才有效"），每项数字标注来源；
- 连接器不可用时**主动、单独告知用户**精度受限，不得一句带过。

## 六、凭据与安全（红线）

1. 凭据（API Key / token）**一律不写入仓库**（见根目录 `.gitignore`）；配置文件放本地客户端目录；
2. 示例配置中的凭据字段是占位符，替换为你自己申请的密钥；
3. 缓存文件（如 `.neodata_token`）加入忽略清单，**切勿提交**；
4. 对外分享移植包前先扫描是否有硬编码密钥（本项目包已扫描，无密钥）。

## 七、本地兜底（开源路线）

无凭据时的零成本起步：`pip install akshare -i https://pypi.tuna.tsinghua.edu.cn/simple` → 使用 `../skills/data-layer/akshare_adapter.py`（`--selftest` 自检；指数行情/中证官方PE/10Y国债/ETF 双源已实测）。更完整的契约与错误码表见 `../skills/data-layer/README.md`。

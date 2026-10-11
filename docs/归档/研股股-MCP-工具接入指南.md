# MCP 工具接入指南

> MCP（Model Context Protocol）是 Anthropic 发起的开放标准：AI 客户端通过统一协议连接外部工具与数据服务。你的工作台只要实现/支持 MCP Client，就能接入任何 MCP Server。

---

## 一、标准配置格式

MCP 配置本质是一份 JSON，任何支持 MCP 的客户端（Claude Desktop / Cursor / Cline / 自研）格式基本通用：

**本地进程式（stdio）——适合本地命令行服务：**
```json
{
  "mcpServers": {
    "my-finance-tool": {
      "command": "npx",
      "args": ["-y", "@some-org/some-mcp-server@latest"],
      "env": { "API_KEY": "你的凭据" }
    }
  }
}
```

**远程服务式（HTTP/SSE）——适合云端 API：**
```json
{
  "mcpServers": {
    "remote-data": {
      "url": "https://api.example.com/mcp",
      "headers": { "Authorization": "Bearer 你的凭据" }
    }
  }
}
```

配置文件位置因客户端而异：Claude Desktop → `claude_desktop_config.json`；Cursor → `.cursor/mcp.json`；自研 → 由你的 Client 代码读取。

---

## 二、本机在用的 5 个连接器清单

以下 5 个连接器均以 MCP 协议接入，完整工具说明已拷贝至 `mcp-docs/` 目录。**注意：它们的授权绑定在 WorkBuddy 账号上，移植到自有工作台需向对应服务商获取独立凭据。**

### 1. dzh-mcp · 大智慧金融数据
- **能力**：A股/港美股/期货/基金行情与K线、财务三表、多维财务选股（40+ 选股器）、板块、股东、分红送转、龙虎榜、大宗交易、研报公告、新闻舆情
- **核心工具**（约 90 个）：
  - `ai-mcp-finance_tools_getStockFinanceData` 财务数据
  - `ai-mcp-finance_tools_findStockCodesBy*` 系列多维选股
  - `ai-mcp-market-quote_tools_getQuoteKline` K线行情
  - `ai-mcp-stock-profile_tools_getF10*` F10 资料系列
- **适用技能**：company-tearsheet、earnings-analysis、comps-valuation、sector-overview

### 2. neodata · NeoData 金融数据库
- **能力**：结构化金融数据 API，覆盖股票/指数/基金/债券/期货/外汇/贵金属/宏观，含行情、估值、财务、资金流、龙虎榜、两融、沪深港通、股东、研报评级、ESG、产业链、宏观日历等
- **核心工具**（约 90 个）：`quote_and_kline`、`income_statement`、`balance_sheet`、`cash_flow`、`valuation`、`fund_holdings`、`margin`、`connect_stats`、`sector_flow_rank`、`macro_cn`、`yield_curve`、`index_valuation` 等
- **适用技能**：dcf-model-builder、initiating-coverage、portfolio-risk、idea-generation（结构化建模首选）

### 3. westock-mcp · 腾讯自选股
- **能力**：行情与资讯、条件选股/策略选股/事件选股、自选股管理、股价提醒、模拟交易
- **核心工具**：
  - `data_*` 系列：kline、quote、finance、fund_flow、lhb、north_holding、chip、hot、report、dividend 等
  - `tool_*` 系列：filter / strategy / ranking / label（选股引擎）
  - `portfolio_*` 系列：paper_trade 模拟交易、watchlist 自选管理
- **适用技能**：idea-generation、morning-note、thesis-tracker（跟踪与提醒场景）

### 4. yanxu · 言序（公众号发布）
- **能力**：微信公众号文章建稿与发布——查公众号、选样式主题、创建草稿、推送草稿箱
- **核心工具**：`list_wechat_accounts`、`list_theme_styles`、`create_article`、`publish_article`
- **适用技能**：morning-note、sector-overview 等产出物的分发渠道

### 5. agent-mail · 智能体邮箱
- **能力**：Agent 专属邮箱，收发邮件、搜索邮件、管理附件
- **核心工具**：`SendMessage`、`ListMessages`、`SearchMessages`、`ForwardMessage`、`ListAttachments`
- **适用技能**：报告定时投递、订阅研报接收

---

## 三、落地建议

1. **先接一个数据源跑通闭环**：推荐 neodata（结构化最全）或 dzh-mcp（中文研报/舆情强），拿到 API 凭据后按上面的 JSON 模板接入
2. **工具不是越多越好**：90+ 工具一次性全挂会挤占上下文且降低路由准确率。建议按技能裁剪——例如做 tearsheet 只挂财务三表 + 估值 + 行情 5~8 个工具
3. **工具文档即提示词**：`mcp-docs/` 里每份 SKILL.md 都写了各工具的参数与适用场景，可直接作为你工作台里"工具选择提示"注入
4. **替代路径**：若暂无服务商凭据，AKShare/Tushare 等开源数据库 + 自封装 MCP Server 是零成本起步方案（Python 有现成 `mcp` SDK）

---

*配置示例中的凭据字段请替换为你自己申请的密钥；切勿将凭据提交到公开仓库。*

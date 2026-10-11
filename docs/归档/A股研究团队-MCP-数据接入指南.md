# MCP / 数据接入指南 · A股研究团队

> 本团队对数据的硬性要求：**所有数字必须来自真实查询，可追溯，禁止编造。**
> 本文件说明本包依赖的 2 条数据链路（westock 主 / neodata 备）如何接进你自己的工作台，以及无凭据时的替代方案。

---

## 一、先理解：MCP 是什么、为什么能"接进来"

MCP（Model Context Protocol）是开放标准：AI 客户端通过统一协议连接外部工具与数据服务。**你的工作台只要实现/支持 MCP Client，就能接入任何 MCP Server**——这也是本包能跨平台移植的底层原因。

标准配置格式（各客户端通用）：

**本地进程式（stdio）**——适合本地命令行服务：
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

**远程服务式（HTTP/SSE）**——适合云端 API：
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

## 二、本团队的两条数据链路

### 链路 A（主）：`westock` 技能 · 腾讯自选股

**包里位置**：`expert-package/skills/westock/`

- `SKILL.md`：技能入口与总体说明
- `SKILL-westock-data.md`（16KB）：**已知标的查数据**——行情、K线、财报、资金流向、技术指标、机构评级、龙虎榜、分红、股东、大宗交易等 `data_*` 系列
- `SKILL-westock-tool.md`（12KB）：**按条件批量选股**——自定义条件筛选 / 预置策略 / 标签 / 事件 / 排行 `tool_*` 系列
- `references/`：`tool-fields-guide.md`、`tool-ai-guide.md`、`data-ai-guide.md`、`data-scenarios-guide.md`（字段字典 + 场景选型指南）
- `scripts/`：4 个已打包的取数脚本（`data-index.js` / `data-vendor.js` / `tool-index.js` / `tool-vendor.js`，合计约 6.3MB，含 vendored 第三方库）

**关键约定**：
- 返回格式 `{ "ok": true|false, "data": ..., "message": "..." }`；`ok: false` 时原样转述 message，禁止编造
- 代码格式：`sh600519`（沪）/ `sz000001`（深）/ `hk00700`（港）/ `usAAPL`（美）；板块 `pt01801080`

**接入方式**：目标平台若支持 MCP，配置 `westock-mcp` 连接器即可；若目标平台是自研 Agent，把 `SKILL-*.md` 作为"工具选择提示"注入，把 `scripts/` 作为取数层调用。

---

### 链路 B（备）：`neodata-financial-search` 技能 · 腾讯 NeoData

**包里位置**：`expert-package/skills/neodata-financial-search/`

- `SKILL.md`：技能入口 + 鉴权流程 + 典型场景表
- `reference.md`：完整能力清单与调用字段
- `scripts/query.py` / `scripts/query.sh`：取数脚本

**能力**：自然语言金融数据召回，覆盖 A股 / 港股 / 美股 / 日股 / 韩股 + 指数 / 板块 / 基金 / 宏观 / 外汇 / 大宗商品 七大类共 60+ 子能力（实时 + 历史）。

**鉴权机制（重要，移植时需替换）**：
- 默认端点：`https://copilot.tencent.com/agenttool/v1/neodata`
- 鉴权优先级：`--token` 参数 > 本地缓存文件（`SKILLS_DIR/.neodata_token`，12 小时有效期）
- 在 WorkBuddy 里，token 由平台鉴权通道（`connect_cloud_service` → `tempToken`）注入
- **移植到你的工作台后这条通道不可用**，需向服务商申请独立凭据，或按下面的替代方案改写

**调用结构（对照替换用）**：
```bash
python3 scripts/query.py --query "用户的查询"
# 或带 token：
bash query.sh --token "<你的凭据>" "贵州茅台股价"
```

---

## 三、三条落地路线（按凭据情况选）

| 路线 | 适用 | 做法 |
|---|---|---|
| ① 有凭据 | 能拿到服务商 API Key | 申请腾讯自选股 / NeoData 独立凭据，按 `scripts/` 的请求结构直接对接；或配置对应 MCP 连接器并用自己账号授权 |
| ② 连接器 | 目标平台支持 MCP 且能自行授权 | 配置 `westock-mcp` / `neodata` MCP Server，工具清单见第四节 |
| ③ 开源替代 | 暂无凭据（零成本起步） | AKShare / Tushare / 东方财富 / 大智慧 等替换，改写 `SKILL.md` 里的调用步骤即可 |

> **关键结论**：8 份成员提示词的分析框架**不依赖具体数据源**，只依赖"能拿到行情 / 财务 / 资金 / 新闻"。换数据源时只需改技能层，人设层与编排层原样保留。

---

## 四、连接器工具清单（供自建 MCP Client 参考）

### westock-mcp · 腾讯自选股
- `data_*` 系列：`kline`、`quote`、`finance`、`fund_flow`、`lhb`、`north_holding`、`chip`、`hot`、`report`、`dividend`、`shareholder`、`notice`、`technical`、`rating` 等
- `tool_*` 系列：`filter` / `strategy` / `ranking` / `label`（选股引擎）
- `portfolio_*` 系列：`paper_trade`、`watchlist`（模拟交易 / 自选管理）

### neodata · NeoData 金融数据库
- 约 90 个结构化工具：`quote_and_kline`、`income_statement`、`balance_sheet`、`cash_flow`、`valuation`、`fund_holdings`、`margin`、`connect_stats`、`sector_flow_rank`、`macro_cn`、`yield_curve`、`index_valuation`、`supply_chain`、`ratings`、`news` 等

### 其他可用连接器（本团队按需挂载，非必需）
- **dzh-mcp · 大智慧**：A股/港美股/期货/基金行情与K线、财务三表、多维财务选股（40+ 选股器）、F10 资料、龙虎榜、大宗交易、研报公告、新闻舆情
- **yanxu · 言序**：微信公众号建稿与发布（`list_wechat_accounts` / `create_article` / `publish_article`），可用于晨报分发
- **agent-mail · 智能体邮箱**：报告定时投递、订阅研报接收

---

## 五、落地建议

1. **先接一条链路跑通闭环**：推荐先从 `westock` 起步（本团队主链路，字段指南最全），跑通"取数 → 成员分析 → 汇编"再考虑加备链路
2. **工具不是越多越好**：几十上百个工具一次性全挂会挤占上下文、降低路由准确率。建议按 Workflow 裁剪——例如跑"个股深度研究"只挂行情 + 财务三表 + 资金流 + 估值 6~10 个工具
3. **工具文档即提示词**：`references/` 与 `SKILL-*.md` 里写了各工具的参数与适用场景，可直接作为你工作台里的"工具选择提示"注入
4. **两个数据源不要混用**：成员提示词里有"禁止混合多数据源"的要求，目的是避免口径不一致引发幻觉；移植时保留这条约束
5. **替代路径**：若暂无服务商凭据，AKShare / Tushare + 自封装 MCP Server 是零成本起步方案（Python 有现成 `mcp` SDK）

---

## 六、安全提示

- 本包已扫描，**无硬编码密钥**；脚本 token 走外部注入或本地缓存文件
- 配置示例中的凭据字段请替换为你自己申请的密钥
- **切勿将凭据提交到公开仓库**；若使用 git 管理，把 `.neodata_token` 等缓存文件加入 `.gitignore`

---

> ⚠️ 以上内容由 AI 基于公开信息整理生成，仅供参考，不构成任何投资建议或个股推荐。投资有风险，决策需谨慎。

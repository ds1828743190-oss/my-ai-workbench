# 研股股专家移植包 · 移植指南

> 打包日期：2026-10-11 ｜ 来源：WorkBuddy 专家插件「严估深 / 研股股」（equity-research）
> 用途：将卖方级股票研究专家的完整能力移植到你自己的工作台

---

## 一、包里有什么

```
研股股-专家移植包/
├── README-移植指南.md            ← 本文件
├── expert-package/               ← 完整专家包（原样拷贝，纯 Markdown，可直接改）
│   ├── agents/
│   │   └── equity-research-expert.md      ★ 主提示词（人设 + 15项职责 + PM七问 + 工作纪律）
│   ├── rules/                             ★ 全局约束规则（3份）
│   │   ├── equity_research_rules.md       研究纪律（数据可追溯/评级/边界）
│   │   ├── equity-valuation-standard.md   估值标准
│   │   └── deliverable-framework.md       交付物框架
│   ├── avatars/expert.png                 头像（可忽略）
│   └── skills/                            ★ 16 个技能包，每个 = 1 个文件夹 + SKILL.md
│       ├── initiating-coverage/           首次覆盖报告（含 7 份 references/ 模板与检查清单）
│       ├── earnings-analysis/             盈利分析（含 3 份 references/）
│       ├── earnings-preview/              业绩前瞻
│       ├── company-tearsheet/             公司速览卡
│       ├── sector-overview/               行业综述
│       ├── morning-note/                  晨会纪要
│       ├── dcf-model-builder/             DCF 估值模型
│       ├── comps-valuation/               可比公司估值
│       ├── model-update/                  模型更新
│       ├── long-short-pitch/              多空推介
│       ├── memo-builder/                  投资备忘录
│       ├── idea-generation/               投资想法筛选
│       ├── portfolio-risk/                组合风险管理
│       ├── event-scenario-analyzer/       事件与情景分析
│       ├── catalyst-calendar/             催化剂日历
│       └── thesis-tracker/                投资逻辑跟踪
└── mcp-docs/                     ← 5 个 MCP 连接器的完整使用文档
    ├── dzh-mcp-大智慧金融数据.md
    ├── neodata-金融数据库.md
    ├── westock-腾讯自选股.md
    ├── yanxu-公众号发布.md
    └── agent-mail-智能体邮箱.md
```

---

## 二、专家能力的三层架构（移植映射表）

这个专家的能力由三层拼装而成，每一层对应你工作台里的不同接法：

| 层 | WorkBuddy 里的机制 | 对应文件 | 移植到你的工作台 |
|---|---|---|---|
| ① 人设层 | Expert 主提示词 | `agents/equity-research-expert.md` + `rules/*.md` | 拼进 System Prompt（常驻） |
| ② 技能层 | Skill 按需加载 | `skills/*/SKILL.md`（及 references/ 子文档） | 按需加载的知识包 / 子工作流 / RAG 文档 |
| ③ 工具层 | MCP 连接器 | `mcp-docs/*.md` + MCP 配置 | 配置 MCP Client 接数据服务 |

**为什么这样分层很关键**：16 个技能全部内容约 60K+ 字，如果一次性塞进 System Prompt 会严重浪费 token 且稀释注意力。原设计采用"渐进式加载"——主提示词只保留一张「职责 → 技能名 → 触发词」对照表，当用户请求命中触发词时才把对应 SKILL.md 载入上下文。**移植时务必保留这个模式**，这是整个专家包的工程核心。

---

## 三、三种典型接法

### 方案 A：Claude Code / Cursor / Cline 类编码客户端
- 主提示词 → 放入项目的 rules 目录（如 `.cursor/rules/research-expert.md`），或 CLAUDE.md / AGENTS.md
- 技能包 → 整个 `skills/` 文件夹拷入项目，按客户端的 skills 机制注册（Claude Code 放 `~/.claude/skills/`）
- MCP → 写入客户端的 MCP 配置（见 `MCP-工具接入指南.md`）

### 方案 B：Dify / Coze 等编排平台
- 主提示词 → 粘贴到应用的"人设与提示词"
- 技能包 → 两个选择：
  1. 每个技能做成一个独立工作流/子应用（推荐常用技能如 tearsheet、morning-note）
  2. 全部上传为知识库文档，在主提示词里写明"命中触发词时检索对应技能文档"
- 工具层 → 平台若有 MCP 支持（Dify 已支持）按指南接入；否则用平台自带的知识检索+HTTP 节点替代

### 方案 C：自研 Agent（LangChain/LangGraph/OpenAI SDK 等）
```python
SYSTEM_PROMPT = read("expert-package/agents/equity-research-expert.md") + "\n\n" + \
                read_all("expert-package/rules/*.md")

SKILLS = {name: read(f"expert-package/skills/{name}/SKILL.md") for name in SKILL_DIRS}

# 对话循环中：先只给模型"技能目录表"（主提示词里自带），
# 模型输出需要某技能时，把该 SKILL.md 注入下一轮上下文
def on_skill_triggered(skill_name):
    inject_context(SKILLS[skill_name])
```

---

## 四、融合落地清单（建议顺序）

1. **先跑通人设层**：把主提示词 + 3 份 rules 拼成 System Prompt，用一个纯对话模型测试"给我做一个宁德时代的公司速览"——此时它应该按 SKILL.md 的结构输出（即使没有实时数据）
2. **再挂技能层**：实现按需加载机制，验证触发词路由是否正确
3. **最后接工具层**：从 1 个 MCP 数据源开始（推荐 neodata 或 dzh-mcp，覆盖面最广），把技能文档里的"数据获取"步骤映射到真实工具调用
4. **补上边界规则**：主提示词末尾的免责声明、[MISSING] 数据标注、不编造数字等纪律，建议原样保留——这是研究报告可信度的底线

---

## 五、不可移植部分（明确告知）

| 资产 | 原因 | 替代方案 |
|---|---|---|
| WorkBuddy 平台系统指令与编排逻辑 | 平台运行配置，不在交付范围 | 用方案 C 自己搭编排 |
| 底层模型能力 | 平台托管 | 接入你选择的任意大模型 API |
| 官方连接器的账号授权 | 绑定 WorkBuddy 账号体系 | 向数据服务商（大智慧/恒生NeoData/腾讯等）申请独立 API 或 MCP 凭据 |

---

*专家包内容为纯 Markdown 文本，可自由修改裁剪。建议保留文件头部的 name/description/触发词元数据格式，便于任何支持 skill 路由的框架解析。*

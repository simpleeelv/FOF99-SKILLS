# FOF99-SKILLS

这个仓库存放好投科技火富牛相关的技能（Skill）。每个 Skill 都是一个独立文件夹，其中的 `SKILL.md` 会告诉 AI 在特定场景下如何工作。

新发布的通用型 Skill 采用统一命名：中文名称包含“火富牛”，英文 slug 使用 `fof99-` 前缀。品牌名称用于搜索和识别；已连接并授权火富牛 MCP 时可自动进入增强模式，未连接时仍可独立使用。

---

## 包含哪些 Skill

| Skill 名称 | 版本 | 主要用途 | 依赖说明 |
|---|---:|---|---|
| [`Fund-Analysis`](skills/Fund-Analysis) | — | 火富牛综合基金分析技能，覆盖公募与私募基金的净值走势、业绩指标、持仓穿透、策略筛选及 FOF 组合分析。 | 需搭配火富牛 MCP 配置使用 |
| [`fof99-fund-report-compliance`](skills/fof99-fund-report-compliance) | 1.0.3 | 火富牛基金报告合规预审助手，检查基金及 FOF 报告中的表述、数据口径、业绩展示、风险披露与专项问题。 | 独立通用；连接火富牛 MCP 后可核验基金数据 |
| [`fof99-fund-diagnosis`](skills/fof99-fund-diagnosis) | 1.0.3 | 火富牛基金深度诊断助手，围绕收益、回撤、修复、风格、管理人与 FOF 穿透生成专业诊断报告。 | 独立通用；连接火富牛 MCP 后可自动补充与核验数据 |
| [`fof99-portfolio-risk-scan`](skills/fof99-portfolio-risk-scan) | 1.0.3 | 火富牛 FOF 组合风险扫描助手，分层检查集中度、回撤、相关性、风险贡献、流动性、压力情景与底层重复暴露。 | 独立通用；仅有持仓可结构扫描，连接火富牛 MCP 后补充量化数据 |

## 双模式数据能力

三个 `fof99-` 技能都会根据当前可用数据自动选择运行方式：

- **火富牛增强模式**：优先调用已授权的只读 MCP 工具，补充基金识别、净值、因子、相关性或私募 FOF 穿透数据。
- **混合核验模式**：以用户材料为主，用 MCP 数据做交叉核验；冲突数据会并列展示，不静默覆盖。
- **通用模式**：无 MCP 或调用失败时，继续使用用户材料、公开资料或手工输入，核心能力不受影响。

所有增强调用均遵循只读原则，不上传报告、不修改平台数据、不执行交易。

## 品牌视觉系统

1.0.3 版本为三个通用型 Skill 增加独立的火富牛视觉规范，并根据任务场景分别优化：

- **基金深度诊断**：研究结论、KPI、净值与回撤图、证据表和适用条件。
- **基金报告合规预审**：风险计数、问题定位、原文与改写分离、发布前条件。
- **FOF 组合风险扫描**：红黄绿灰灯号、数据覆盖率、风险矩阵、优先事项和复核计划。

视觉规范支持 ECharts 及其他可用图表能力；纯 Markdown 会自动采用结构化表格和状态标记，不依赖特定渲染工具。

---

## 怎么安装？

### 方式一：命令行安装（推荐）

安装 [Node.js](https://nodejs.org) 后，在终端运行所需 Skill：

```bash
# 火富牛综合基金分析
npx skills add simpleeelv/FOF99-SKILLS/Fund-Analysis

# 火富牛基金报告合规预审
npx skills add simpleeelv/FOF99-SKILLS/fof99-fund-report-compliance

# 火富牛基金深度诊断
npx skills add simpleeelv/FOF99-SKILLS/fof99-fund-diagnosis

# 火富牛 FOF 组合风险扫描
npx skills add simpleeelv/FOF99-SKILLS/fof99-portfolio-risk-scan
```

安装到全局时增加 `-g` 参数，例如：

```bash
npx skills add simpleeelv/FOF99-SKILLS/fof99-fund-diagnosis -g
```

### 方式二：让 AI 自动安装

> 帮我安装 GitHub 上的 Skill：`simpleeelv/FOF99-SKILLS/fof99-fund-diagnosis`

### 方式三：手动导入

下载相应 Skill 文件夹，并导入其中的 `SKILL.md` 和 `references/`。

---

## 仓库结构

```text
FOF99-SKILLS/
├── README.md
├── skills/
│   ├── Fund-Analysis/
│   │   └── SKILL.md
│   ├── fof99-fund-report-compliance/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── fof-review-checklist.md
│   │       ├── fof99-mcp-routing.md
│   │       ├── fof99-visual-style.md
│   │       └── report-template.md
│   ├── fof99-fund-diagnosis/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── diagnosis-methodology.md
│   │       ├── fof-diagnosis.md
│   │       ├── fof99-mcp-routing.md
│   │       ├── fof99-visual-style.md
│   │       └── report-template.md
│   └── fof99-portfolio-risk-scan/
│       ├── SKILL.md
│       └── references/
│           ├── fof99-mcp-routing.md
│           ├── fof99-visual-style.md
│           ├── report-template.md
│           ├── risk-methodology.md
│           └── signal-framework.md
└── mcp/
    ├── README.md
    └── mcp.json.example
```

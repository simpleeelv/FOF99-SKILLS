# FOF99-SKILLS

这个仓库存放好投科技火富牛相关的技能（Skill）。每个 Skill 都是一个独立文件夹，其中的 `SKILL.md` 会告诉 AI 在特定场景下如何工作。

新发布的通用型 Skill 采用统一命名：中文名称包含“火富牛”，英文 slug 使用 `fof99-` 前缀。品牌名称用于搜索和识别，不代表必须使用火富牛平台或 MCP。

---

## 包含哪些 Skill

| Skill 名称 | 主要用途 | 依赖说明 |
|---|---|---|
| [`Fund-Analysis`](skills/Fund-Analysis) | 火富牛综合基金分析技能，覆盖公募与私募基金的净值走势、业绩指标、持仓穿透、策略筛选及 FOF 组合分析。 | 需搭配火富牛 MCP 配置使用 |
| [`fof99-fund-report-compliance`](skills/fof99-fund-report-compliance) | 火富牛基金报告合规预审助手，检查基金及 FOF 报告中的表述、数据口径、业绩展示、风险披露与专项问题。 | 独立通用，可使用用户材料或任意可用数据源 |
| [`fof99-fund-diagnosis`](skills/fof99-fund-diagnosis) | 火富牛基金深度诊断助手，围绕收益、回撤、修复、风格、管理人与 FOF 穿透生成专业诊断报告。 | 独立通用，不要求特定平台、MCP 或数据库 |
| [`fof99-portfolio-risk-scan`](skills/fof99-portfolio-risk-scan) | 火富牛 FOF 组合风险扫描助手，分层检查集中度、回撤、相关性、风险贡献、流动性、压力情景与底层重复暴露。 | 独立通用；仅有持仓也可执行结构扫描 |

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
│   │       └── report-template.md
│   └── fof99-fund-diagnosis/
│       ├── SKILL.md
│       └── references/
│           ├── diagnosis-methodology.md
│           ├── fof-diagnosis.md
│           └── report-template.md
│   └── fof99-portfolio-risk-scan/
│       ├── SKILL.md
│       └── references/
│           ├── report-template.md
│           ├── risk-methodology.md
│           └── signal-framework.md
└── mcp/
    ├── README.md
    └── mcp.json.example
```

# FOF99-SKILLS

这个仓库存放好投科技火富牛相关的技能（Skill）。每个 Skill 都是一个独立文件夹，其中的 `SKILL.md` 会告诉 AI 在特定场景下如何工作。

---

## 包含哪些 Skill

| Skill 名称 | 主要用途 | 适用说明 |
|---|---|---|
| [`Fund-Analysis`](skills/Fund-Analysis) | 火富牛综合基金分析技能，覆盖公募与私募基金的净值走势、业绩指标、持仓穿透、策略筛选及 FOF 组合分析。 | 需搭配火富牛 MCP 配置使用 |
| [`fund-report-compliance`](skills/fund-report-compliance) | 基金报告合规预审助手，检查基金及 FOF 报告中的表述、数据口径、业绩展示、风险披露与专项问题，并输出专业预审报告及修改建议。 | 适用于投研、尽调、业绩、归因、客户及路演材料的发布前预审 |

---

## 怎么安装？

### 方式一：命令行安装（推荐）

安装 [Node.js](https://nodejs.org) 后，在终端运行：

```bash
# 火富牛综合基金分析
npx skills add simpleeelv/FOF99-SKILLS/Fund-Analysis

# 基金报告合规预审
npx skills add simpleeelv/FOF99-SKILLS/fund-report-compliance
```

安装到全局时增加 `-g` 参数：

```bash
npx skills add simpleeelv/FOF99-SKILLS/fund-report-compliance -g
```

### 方式二：让 AI 自动安装

> 帮我安装 GitHub 上的 Skill：`simpleeelv/FOF99-SKILLS/fund-report-compliance`

### 方式三：手动导入

下载相应 Skill 文件夹，并导入其中的 `SKILL.md`、`agents/` 和 `references/`。

---

## 仓库结构

```text
FOF99-SKILLS/
├── README.md
├── skills/
│   ├── Fund-Analysis/
│   │   └── SKILL.md
│   └── fund-report-compliance/
│       ├── SKILL.md
│       ├── agents/
│       │   └── openai.yaml
│       └── references/
│           ├── fof-review-checklist.md
│           └── report-template.md
└── mcp/
    ├── README.md
    └── mcp.json.example
```

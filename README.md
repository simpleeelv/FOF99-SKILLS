# FOF99-SKILLS
这个仓库存放了好投科技火富牛相关的技能（Skill）。
每个 Skill 都是一个文件夹，里面包含一个 `SKILL.md` 指令文件，告诉 AI 在特定场景下该怎么做。
---
## 包含哪些 Skill
| Skill 名称 | 干什么用的 | 适用场景 |
|---|---|---|
| `Fund-Analysis` | 火富牛综合基金分析技能，覆盖私募和公募基金的净值走势、业绩指标、持仓穿透、策略筛选与FOF组合分析。当用户需要分析基金、比较业绩、查看持仓、筛选基金或生成分析报告时调用。|需搭配火富牛MCP配置使用|
---
## 怎么安装？
### 方式一：命令行安装（推荐）
装了 [Node.js](https://nodejs.org) 之后，在终端里运行：

- 装到当前项目（跟着项目走）：
```bash
npx skills add simpleeelv/FOF99-SKILLS/Fund-Analysis
```

- 装到全局（所有项目都能用）：加 `-g` 参数
```bash
npx skills add simpleeelv/FOF99-SKILLS/Fund-Analysis -g
```
安装后会自动放到 AI 工具的 skills 目录里，不用手动操作。

### 方式二：跟AI对话，让AI自动装

> 帮我安装 GitHub 上的 skill：simpleeelv/FOF99-SKILLS/Fund-Analysis

AI 会自动拉取安装。

### 方式三：手动导入：手动上传 SKILL.md 文件
---

## 仓库结构

```
FOF99-SKILLS/
├── README.md                  ← 你正在看的这个文件
└── Fund-Analysis/
    └── SKILL.md           ← 技能的指令文件
```

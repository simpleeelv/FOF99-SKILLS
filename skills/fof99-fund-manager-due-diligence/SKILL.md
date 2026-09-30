---
name: fof99-fund-manager-due-diligence
description: Research and assess Chinese private fund managers and produce a self-contained, source-backed Chinese HTML due-diligence report with a separate internal workpaper. Use for 私募基金管理人尽调、管理人初筛、准入尽调、年度复核、策略尽调、核心团队与股权核验、产品全景与代表产品业绩、合规诚信与舆情核查、尽调访谈问题 or a polished manager due-diligence report. When authorized FOF99 MCP tools are available, use them for structured manager, product, NAV, performance, integrity, and risk data; otherwise work independently with user materials, official disclosures, other connected sources, and traceable public information. Preserve evidence provenance, distinguish manager statements from verified facts, and never invent unavailable private data.
---

# 火富牛-私募基金管理人尽调

> 版本：1.0.0

围绕中国私募基金管理人完成证据驱动的策略尽调或机构级尽调，并将正式报告与内部研究底稿分开交付。本 Skill 提供决策支持，不替代法律意见、审计鉴证、监管判断或投资建议。

“火富牛”用于品牌识别，并代表可选的结构化数据增强能力。未连接火富牛 MCP 时，继续使用用户材料、其他授权连接、官方披露和可追溯公开信息；不得因缺少 MCP 而中止，也不得把未取得数据解释为零或无风险。

## 先确定范围

识别并记录：

- 管理人法定名称、登记编号及同名主体；
- 尽调目的、报告读者、数据截止日和保密要求；
- 重点策略、产品及用户提供的材料；
- 交付形式：对话摘要、Markdown，或正式 HTML 与内部 HTML 底稿。

默认范围为中国私募证券基金管理人。用户明确要求股权／创投管理人尽调时，改用项目、退出、估值、DPI、RVPI、TVPI、IRR、基金生命周期和关键人条款，不套用证券基金净值指标。

默认使用 `strategy` 模式，聚焦管理人、团队、策略、产品全景、代表性业绩和重大风险。只有用户明确提出准入、投委会、年度复核、运营尽调或合规复核时，才使用 `institutional` 模式并增加运营控制、条件清单和持续监测。

## 数据路由

先服从用户对联网、数据源、保密和时间范围的明确限制，再选择：

- **火富牛增强模式**：存在已授权火富牛 MCP 查询工具时，优先获取结构化管理人、产品、净值、指标、诚信和风险数据。
- **混合核验模式**：用户材料与 MCP 同时存在时，以材料对应的业务事实为起点，用 MCP 与官方来源交叉核验；冲突并列保留。
- **通用模式**：MCP 不可用、未授权、未命中或结果不完整时，使用用户材料、官方披露、其他授权来源和可追溯公开信息继续完成。

只有进入增强或混合模式时，读取 [火富牛 MCP 路由](references/fof99-mcp-routing.md)。只使用查询、比较和只读计算工具；禁止上传净值、修改平台数据、创建产品或执行交易。

## 高效工作流

### 1. 建立证据底稿

将用户文件中的事实、管理人陈述和外部核验结果分开。每项影响结论的事实至少记录：主题、事实、来源、来源类型、数据／发布日期、检索日期、证据状态、限制和冲突。

开始实质研究前读取 [尽调逻辑与报告框架](references/due-diligence-framework.md)。监管、登记、处罚和司法事实必须优先核验当前官方来源；商业平台只作补充线索。

### 2. 按决策价值查询

不要一次加载或查询全部模块：

1. 先核验身份、登记、股权、核心团队、策略及重大风险；
2. 再获取一次完整产品目录的元数据，记录分页和覆盖范围；
3. 先统计产品状态、策略、成立时间和净值新鲜度，再选择代表产品；
4. 默认最多选择 3 只代表产品，净值预检成功后才查询指标和比较数据；
5. 只有结论可能改变时才追加同业、滚动、年度或全产品查询。

使用火富牛 MCP 查询产品目录、净值或业绩时，遵守 [火富牛 MCP 路由](references/fof99-mcp-routing.md) 中的检索档位与停止条件。相同工具、对象、参数和时间区间只调用一次并复用结果。分页先读第一页与总量；需要超过 1,000 条时先征得用户同意。

### 3. 分析与挑战

使用 [尽调逻辑与报告框架](references/due-diligence-framework.md) 分析证据。必须区分：

- `事实`：来源直接支持的内容；
- `分析`：事实对策略、团队、容量、业绩或风险的含义；
- `结论`：在当前证据范围内的判断；
- `待核验`：会改变判断但尚未取得的材料。

重点检查身份与股权冲突、关键人依赖、策略与实现不一致、选择性业绩、净值停更、规模与容量错配、提前清算、重大监管／诚信事项以及来源间矛盾。

评分不是默认要求。只有用户需要量化摘要或机构模板要求评分时，才使用统一框架中的可选评分规则。缺失信息不得计零，也不得因为未发现负面记录而给高分；高严重度事实可覆盖总分。

### 4. 形成双层交付

正式报告只展示决策相关事实、分析、风险、结论和重要限制；内部底稿保留数据路径、工具调用、失败记录、证据台账、计算过程、访谈问题、补充材料和后续任务。

需要 HTML 文件交付时读取 [报告数据契约](references/report-data-contract.md)，并执行统一框架中的双层交付规则。不要把 MCP 工具名、调用预算、失败日志或原始研究任务写进正式报告。

### 5. 生成与验证报告

正式报告与内部底稿使用同一个 HTML 生成器：

```bash
python3 scripts/generate_due_diligence_html.py \
  --input /absolute/path/report-data.json \
  --output /absolute/path/manager-dd.html
```

默认同时生成 `manager-dd-workpaper.html`。只有用户明确不需要内部底稿时才使用 `--no-workpaper`。

生成强调排版的报告时读取 [火富牛尽调视觉规范](references/fof99-visual-style.md)。生成器只使用 Python 标准库，输出自包含 HTML，不需要 `reportlab`、浏览器自动化、CDN、字体包或图表库。

交付前：

1. 检查身份、截止日、来源、关键数字和结论是否一致；
2. 确认正式报告没有工具日志、原始证据台账或内部待办；
3. 确认底稿记录查询范围、分页、失败、计算和未解决事项；
4. 在桌面端、窄屏和 A4 打印预览中检查表格、图表、链接与分页；
5. 确认 HTML 可离线打开，且没有 CDN、外部脚本、字体或图片依赖。

## 输出底线

- 每项重大事实都要有来源，或明确标注为管理人陈述／第三方线索／未取得。
- 公开未检索到记录不等于不存在违规、诉讼、争议或风险。
- 业绩必须说明区间、频率、净值来源、实盘／模拟、费前／费后及覆盖范围。
- 代表产品不得描述为全部产品；披露选择规则和样本偏差。
- 舆情线索不等于已核实事实，监管措施与一般新闻分开处理。
- 不输出认证凭据、请求头、连接地址或超出用户授权范围的私有数据。
- 报告必须注明：`仅供尽职调查参考，不构成投资建议、法律意见或审计鉴证。`

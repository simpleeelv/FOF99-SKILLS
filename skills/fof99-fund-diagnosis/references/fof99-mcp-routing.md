# 火富牛 MCP 路由｜基金深度诊断

仅在当前工具目录中存在已授权的火富牛 MCP 查询工具时使用本文件。优先匹配 `mcp__fof99_mcp_mall_stream__*`，也兼容 `mcp__fof99_mcp_mall__*`；按工具名称后缀和实际参数说明识别能力，不假设所有客户端前缀完全相同。

## 1. 调用边界

- 只调用查询类工具。禁止调用名称或说明含上传、写入、创建、更新、删除或交易执行的工具。
- 用户明确要求仅使用其材料时，不调用 MCP。
- 私有组合、自建基金或团队数据只在当前授权范围内查询，不向其他服务转发。
- 先检查 `isError`、`error`、空数组、截止日和关键字段，再采用结果。
- 工具无匹配、无权限、超时或无数据时，记录未命中项并切换通用路径；不要连续重复同一失败调用。

## 2. 身份与日期

| 目的 | 工具后缀 | 规则 |
|---|---|---|
| 获取服务器时间 | `get_current_time` | 需要“截至目前”时调用，用作检索日期，不代替净值日期 |
| 基金名称解析 | `get_fund_code` | 名称转代码并区分私募／公募；代码已明确时不重复查询 |
| 私募管理人解析 | `get_company_code` | 仅在需要管理人详情时调用 |
| 组合名称解析 | `get_combi_id_encrypt` | 用户分析已授权实盘、模拟或直投组合时调用 |

唯一匹配且基金名称、类型一致时可继续；同名、多份额、类型冲突或匹配不稳定时列出候选并请求确认。

## 3. 单基金核心数据

| 数据 | 私募 | 公募 |
|---|---|---|
| 基本信息 | `fund_info` | `gm_fund_info` |
| 区间净值 | `fund_platform_price` 或 `fund_company_price` | `gm_fund_price` |
| 业绩指标 | `get_fund_factor` | `get_gm_fund_factor` |

私募净值先确认平台净值与团队净值的来源和口径；两者冲突时并列显示并请求用户确认主口径。公募或私募指标调用应显式传入分析区间、净值类型和可得更新频率。

指标接口返回的默认基准可能是系统映射指数，不一定等于合同披露的复合业绩比较基准。必须将 `fund_info`／`gm_fund_info` 中的业绩基准与指标结果中的指数名称对照；不一致时将工具结果标为“参考指数比较”，不得写成正式基准比较。

## 4. 基准、比较与风格

- 使用 `get_index_code` 解析指数，使用 `index_price` 和 `get_index_factor` 获取区间数据。
- 使用 `compare_returns`、`compare_annual`、`compare_factors` 和 `compare_roll_analysis` 做多区间或滚动比较。
- 使用 `compare_corr_matrix` 检查基金、指数及可得因子之间的相关性。
- 使用 `get_style_factor`、`stock_factor_cne5`、`stock_factor_cne6` 或 `future_factor` 仅在策略与数据适配时补充风格证据，不把相关性直接解释为因果归因。

多基金比较时，公募代码传 `gm_fund_code`，私募代码传 `sm_fund_code`，自建基金使用其专属 `fund_id`。统一起止日、频率、币种与净值类型。

## 5. 管理人与 FOF

- 私募管理人可按需使用 `company_info`、`company_detail`、`company_manager`、`company_scale`、`company_shareholder`、`company_risk_sincerity` 和 `company_risk_tip`。
- `fof_sub_fund` 仅用于私募 FOF 的指定日期穿透；不得泛化为公募 FOF 持仓工具。
- `fof_sub_fund_deals` 用于私募 FOF 底层交易记录。超过工具提示的分页上限时先征得用户同意。
- 对已授权直投组合，可使用 `fof_invest_customer_price`、`fof_invest_customer_factor` 和 `fof_invest_fund_scale`。
- 穿透结果为空时标记“火富牛当前无可用穿透数据”，继续用用户持仓、定期报告或官方披露，不推断为零持仓。

## 6. 图表与来源

`render_echarts` 只在可用且需要图片时使用，参数必须是严格 JSON，不能包含 JavaScript 函数。不可用时使用当前环境的图表能力或 Markdown 表格。

报告至少记录：运行模式、工具数据截止日、净值来源、净值类型、更新频率、比较基准、未命中项及与用户材料的冲突。将来源写成“火富牛 MCP”仅限实际采用的字段。

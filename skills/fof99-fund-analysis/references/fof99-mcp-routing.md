# 火富牛 MCP 路由｜综合基金分析

仅在当前工具目录存在已授权的火富牛 MCP 查询工具时使用。优先匹配 `mcp__fof99_mcp_mall_stream__*`，也兼容 `mcp__fof99_mcp_mall__*`；根据工具后缀和实际参数说明识别能力，不假设所有客户端前缀一致。

## 安全边界

- 只调用查询、比较、计算和图表渲染工具。
- 不调用名称或说明包含上传、写入、新增、修改、删除、下单或交易执行的工具。
- 不在报告、日志或示例中输出认证凭据、请求头或连接地址。
- 用户提供的组合权重、现金、负债和实际持仓优先于平台候选数据；冲突时并列展示。
- 鉴权失败、无匹配、空数据或超时后，切换到混合或通用模式，不要求用户必须配置 MCP。

## 查询路由

| 任务 | 优先工具后缀 | 注意事项 |
|---|---|---|
| 基金名称解析 | `get_fund_code` | 读取代码与公募／私募类型；多候选时请用户确认 |
| 管理人解析 | `get_company_code` | 后续再查询管理人详情、规模或旗下基金 |
| 私募基本信息 | `fund_info` | 核验策略、管理人、成立日期和基准等可得字段 |
| 公募基本信息 | `gm_fund_info` | 核验份额、类型、管理人和基准等可得字段 |
| 私募净值序列 | `fund_company_price` 或 `fund_platform_price` | 明确团队净值／平台净值来源，不静默混用 |
| 公募净值序列 | `gm_fund_price` | 使用起止日期获取时间序列 |
| 自建基金净值 | `personal_fund_price` | 必须直接提供自建基金 ID，不能用普通基金代码替代 |
| 单基金指标 | `get_fund_factor`、`get_gm_fund_factor`、`personal_fund_factor` | 明确区间、净值类型、频率与基准 |
| 混合类型比较 | `compare_view`、`compare_factors`、`compare_returns`、`compare_annual`、`compare_corr_matrix`、`compare_roll_analysis` | 按对象类型填入对应代码字段，统一公共区间与频率 |
| 私募筛选 | `fund_strategy_list` 或 `filter_sm_fund` | 记录筛选条件、排序字段、页码和样本范围 |
| 公募筛选 | `filter_gm_fund` | 记录基金类型、指标区间、规模、风险等级等条件 |
| 管理人产品与规模 | `company_fund_list`、`company_scale` | 排名或比较前确认披露日期和口径 |
| 私募 FOF 穿透 | `fof_sub_fund` | 只适用于可识别的私募 FOF；无数据不是零持仓 |
| 直投组合 | `fof_invest_customer_price`、`fof_invest_customer_factor`、`fof_invest_fund_scale` | 需要已授权的组合 ID；无权限时使用用户材料 |
| 估值表状态 | `fund_valuation_info` | 只反映可得估值表信息和解析状态 |
| 图表渲染 | `render_echarts` | 可选；参数必须是严格 JSON，不得包含 JavaScript 函数 |

## 数据选择规则

- `multiple_fund_company_price`、`multiple_fund_platform_price`、`gm_multiple_fund_price` 只查询指定日期快照，不得当作区间净值序列。
- 多基金长期走势优先使用 `compare_view`，或分别查询单基金时间序列后再对齐。
- 单基金因子接口返回的默认基准不一定等于合同或官方业绩比较基准；正式结论前核验基金资料。
- `fof_sub_fund` 仅用于私募 FOF。公募 FOF 的底层持仓使用用户材料、基金定期报告或其他可追溯披露。
- 平台排名、评分或筛选结果只作为候选证据，不直接转化为推荐。

## 调用后的披露

记录已调用查询类别、实际覆盖对象、数据截止日、未命中项和冲突项。不要堆砌工具原始返回；只提取完成用户任务所需字段。分页结果未完整获取时，明确写明当前页和样本覆盖范围。

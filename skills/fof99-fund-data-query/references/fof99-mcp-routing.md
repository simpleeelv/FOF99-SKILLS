# 火富牛 MCP 路由｜基金数据查询与核验

仅在当前工具目录存在已授权的火富牛 MCP 查询工具时使用。优先匹配 `mcp__fof99_mcp_mall_stream__*`，也兼容 `mcp__fof99_mcp_mall__*`；以工具后缀、描述和实际参数为准。

## 只读与最小化原则

- 只调用查询、比较和只读计算工具。
- 禁止调用上传、写入、新增、修改、删除、调仓或交易执行工具。
- 只查询用户任务所需对象和时间范围；不批量拉取无关的授权组合或团队数据。
- 查询失败、无权限、未命中或空数据时记录状态并降级，不重复暴力调用。

## 基金与管理人

| 任务 | 优先工具后缀 | 说明 |
|---|---|---|
| 当前日期 | `get_current_time` | 用于查询时点，不等于数据截止日 |
| 基金名称解析 | `get_fund_code` | 返回代码与公募／私募类型；多候选需确认 |
| 管理人名称解析 | `get_company_code` | 获取私募管理人登记编号 |
| 私募基本信息 | `fund_info` | 适用于私募基金 |
| 公募基本信息 | `gm_fund_info` | 适用于公募基金 |
| 管理人基本信息 | `company_info`、`company_detail` | 根据登记编号查询 |
| 旗下基金 | `company_fund_list` | 注意运作状态、管理类型和分页范围 |
| 团队与高管 | `company_manager`、`company_senior`、`company_senior_list` | 区分基金经理、核心人员与法人履历 |
| 规模 | `company_scale` | 核验披露日期；不默认视为完整历史序列 |
| 监管／舆情 | `company_opinion_list` | `type=1` 为监管措施，`type=2` 为舆情信息，不称作路演纪要 |
| 诚信与机构提示 | `company_risk_sincerity`、`company_risk_tip` | 记录来源、日期和分页范围 |

## 净值与指标

| 对象 | 净值序列 | 区间指标 |
|---|---|---|
| 私募基金 | `fund_company_price` 或 `fund_platform_price` | `get_fund_factor` |
| 公募基金 | `gm_fund_price` | `get_gm_fund_factor` |
| 自建基金 | `personal_fund_price` | `personal_fund_factor` |
| 直投组合 | `fof_invest_customer_price` | `fof_invest_customer_factor` |
| 模拟组合 | `simulated_combi_price` | `simulated_combi_factor` |
| 实盘组合 | `live_trading_portfolio_price` | `live_trading_portfolio_factor` |

- 自建基金必须使用自建基金 ID，不能用普通基金代码替代。
- `multiple_fund_company_price`、`multiple_fund_platform_price`、`gm_multiple_fund_price` 只返回指定日期快照，不得当作区间净值序列。
- 多对象时间序列与比较优先使用 `compare_view`，指标用 `compare_factors`，收益分期用 `compare_returns`／`compare_annual`，相关性用 `compare_corr_matrix`，滚动数据用 `compare_roll_analysis`。
- 单基金指标接口的默认比较指数不一定等于正式业绩比较基准；必要时用基金资料核验。

## 持仓、组合与市场

| 任务 | 优先工具后缀 | 边界 |
|---|---|---|
| 私募 FOF 穿透 | `fof_sub_fund`、`fof_sub_fund_deals` | 无数据不代表零持仓；不适用于公募 FOF |
| 直投组合规模与持仓 | `fof_invest_fund_scale` | 需要已授权组合 ID 和明确截止日 |
| 模拟／实盘组合持仓 | `simulated_combi_position`、`live_trading_portfolio_position` | 只查询用户有权限的组合 |
| 估值表状态 | `fund_valuation_info` | 返回估值日期、来源、更新时间和解析状态 |
| 指数代码与行情 | `get_index_code`、`index_price`、`multiple_index_price` | 多指数接口为指定日期快照 |
| 期货升贴水／基差 | `get_futures_discount_rate`、`get_future_basis` | 明确合约、日期和计算口径 |

公募 FOF 持仓使用用户材料、基金定期报告或其他可追溯披露。工具返回空值、错误或字段缺失时保留原始状态，不自行推断。

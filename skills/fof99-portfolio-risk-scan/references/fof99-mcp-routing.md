# 火富牛 MCP 路由｜FOF 组合风险扫描

仅在当前工具目录存在已授权的火富牛 MCP 查询工具时使用。优先匹配 `mcp__fof99_mcp_mall_stream__*`，也兼容 `mcp__fof99_mcp_mall__*`；按工具后缀和实际参数说明识别能力。

## 1. 安全与事实边界

- 只调用查询工具。禁止上传净值或组合、写入数据、创建或修改组合、执行交易。
- 用户提供的实际权重、金额、现金、负债、杠杆、风险预算和流动性需求优先于平台推断。
- 私有、自建、团队和组合数据只在当前授权范围内查询，不向其他服务转发。
- 调用后检查错误、空数据、日期、覆盖率和关键字段。单项失败只降低该维度置信度。

## 2. 标的解析

- 基金名称使用 `get_fund_code` 解析并区分公募／私募；代码明确时不重复查询。
- 已授权实盘、模拟或直投组合名称使用 `get_combi_id_encrypt` 获取加密 ID，并核对组合类型。
- 同名、多份额、类型冲突或组合匹配不唯一时请求确认，不自行选择。

## 3. 持仓与组合数据

| 对象 | 净值／指标 | 持仓或规模 |
|---|---|---|
| 私募基金 | `fund_platform_price` 或 `fund_company_price`；`get_fund_factor` | `fund_info` |
| 公募基金 | `gm_fund_price`；`get_gm_fund_factor` | `gm_fund_info` |
| 直投组合 | `fof_invest_customer_price`；`fof_invest_customer_factor` | `fof_invest_fund_scale` |
| 实盘组合 | `live_trading_portfolio_price` | `live_trading_portfolio_position` |
| 模拟组合 | `simulated_combi_price` | `simulated_combi_position` |
| 自建基金 | `personal_fund_price`；`personal_fund_factor` | 使用专属 `fund_id`，不能由 `get_fund_code` 取得 |

多基金指定日期的 `multiple_fund_platform_price`、`multiple_fund_company_price` 和 `gm_multiple_fund_price` 只是快照，不是区间序列，不能单独支持回撤、波动或相关性计算。

## 4. 批量比较与相关性

- `compare_corr_matrix`：相关性矩阵和超额相关性矩阵。
- `compare_factors`：收益、波动、回撤、修复、Alpha、Beta、VaR 等指定指标。
- `compare_roll_analysis`：滚动收益、波动、回撤、相关性和风险调整指标。
- `compare_returns`：周、月、季度、半年度、年度或区间收益。
- `compare_annual`：跨年度收益、波动和回撤。

参数按标的类型分别传入：公募 `gm_fund_code`、私募 `sm_fund_code`、自建基金 `fund_id`、实盘组合 `combi_id`、模拟组合 `fo_combi_id`。统一分析区间、净值类型和频率；不同频率优先降至共同可靠频率。

MCP 返回相关性后仍需检查重叠样本、低频估值和估值滞后。低相关不自动等于有效分散。系统默认指数不一定等于每只基金的正式复合业绩基准。

## 5. FOF 穿透与流动性

- `fof_sub_fund` 仅用于私募 FOF 指定日期的底层基金、期货和股票持仓。
- `fof_sub_fund_deals` 用于私募 FOF 底层交易记录；超过工具提示的分页上限前征得用户同意。
- 公募 FOF 的穿透不能依赖上述工具，改用用户材料、基金定期报告或其他正式披露。
- 返回“无数据”表示当前无可用穿透记录，不表示零持仓或无集中风险。
- MCP 基础信息和净值接口通常不能完整替代锁定期、通知期、赎回到账、额度、暂停和侧袋条款；流动性扫描仍需合同或产品要素表。

## 6. 覆盖率与降级

分别报告：基金身份匹配率、净值覆盖率、指标覆盖率、相关性覆盖率、穿透覆盖率和条款覆盖率。只有实际采用的字段才能标注“火富牛 MCP”。

无权限、无匹配、空数据或超时后，停止重复同类失败调用，转用用户文件、其他连接数据源或公开披露。缺失项进入灰灯，不得并入绿灯或推断为低风险。

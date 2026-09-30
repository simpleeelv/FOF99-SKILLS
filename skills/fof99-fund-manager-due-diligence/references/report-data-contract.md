# 尽调报告数据契约

仅在生成 HTML 文件时读取。数据使用 UTF-8 JSON；顶层必须为对象。只填充有真实证据支持的字段，不要求填满所有可选章节。

## 最小正式报告

```json
{
  "meta": {
    "manager_name": "管理人法定名称",
    "title": "火富牛-私募基金管理人尽调报告",
    "report_mode": "strategy",
    "purpose": "管理人初筛",
    "report_date": "YYYY-MM-DD",
    "data_cutoff": "YYYY-MM-DD",
    "confidentiality": "内部参考"
  },
  "executive_summary": {
    "summary": "一段摘要",
    "overall_view": "建议继续尽调 / 有条件推进 / 暂缓 / 不建议推进",
    "evidence_completeness": "充分 / 部分充分 / 不足",
    "top_risk": "高 / 中 / 低 / 信息不足",
    "key_observations": ["观察一"]
  },
  "company": {},
  "team": [],
  "strategy": {},
  "product_universe": {},
  "products": [],
  "performance": {},
  "risk_review": [],
  "conclusion": {},
  "report_disclosures": []
}
```

`meta.manager_name` 为唯一强制字段。其他章节按实际证据填充；空章节应省略，不用占位文本冒充研究结果。

## 正式报告字段

| 字段 | 类型 | 用途 |
|---|---|---|
| `timeline` | list | 关键事件，含日期、事件、影响和状态 |
| `shareholders` | list | 股东、类型、比例、出资与证据状态 |
| `governance` | object | 实控人、治理结构、关联关系和重大未决事项 |
| `team` | list | 姓名、角色、经历、策略职责、关键人风险 |
| `strategy` | object | 策略类型、概述和策略维度 |
| `product_universe` | object | 总量、分页、状态、策略和净值覆盖 |
| `products` | list | 代表产品及其选择理由、状态和净值日期 |
| `performance` | object | 口径、指标、净值序列和分析 |
| `risk_review` | list | 维度、事实、分析、等级、依据和边界 |
| `conclusion` | object | 总体意见、理由、适用边界和重要条件 |
| `report_disclosures` | list | 数据范围、未取得事项和免责声明 |

`performance.nav_series` 的每项至少包含 `date` 与数值型 `nav`；基准可使用数值型 `benchmark`。序列按日期升序，来源不同的净值不得无标记拼接。

## 仅内部底稿字段

| 字段 | 用途 |
|---|---|
| `route_notice` | 数据路线和降级说明 |
| `generation_audit` | 查询范围、工具状态、调用、计算和失败 |
| `product_deep_dive_queue` | 延后的产品业绩专项任务 |
| `scorecard` | 可选评分证据及置信度 |
| `contradictions` | 来源冲突和待确认事项 |
| `external_cross_checks` | 商业平台等交叉核验 |
| `operations` | 运营尽调检查 |
| `gaps` | 数据缺口和最小补充材料 |
| `interview_questions` | 分优先级的访谈问题 |
| `monitoring_triggers` | 触发条件与复核动作 |
| `mcp_gap_map` | 缺失数据、可用工具和决策价值 |
| `evidence` | 证据台账 |

即使 `report_mode` 为 `institutional`，原始工具日志、凭据、请求头和内部调用预算仍不得进入正式报告。

## 证据台账

`evidence` 每项建议包含：

```json
{
  "id": "E-001",
  "topic": "登记信息",
  "fact": "来源直接支持的事实",
  "source": "来源名称",
  "url": "https://...",
  "source_type": "官方 / MCP / 管理人材料 / 第三方",
  "source_date": "YYYY-MM-DD",
  "retrieved_at": "YYYY-MM-DD",
  "status": "已核验 / 管理人陈述 / 第三方线索 / 存在冲突 / 未取得",
  "limitation": "证据限制"
}
```

## 生成前检查

- 日期采用 `YYYY-MM-DD`，不能用报告日代替净值日。
- 百分数、金额和规模同时提供单位。
- 所有列表字段必须为数组，对象字段必须为对象。
- 不把空字符串、`0`、`-` 混合用于表达缺失；缺失用空值并在状态或限制中说明。
- 正式结论引用的关键事实必须能映射到证据台账或正式来源。

#!/usr/bin/env python3
"""Generate self-contained FOF99 private fund manager DD HTML files."""

from __future__ import annotations

import argparse
import html
import json
import math
from datetime import date
from pathlib import Path
from typing import Any, Iterable


RED = "#E8663C"
DEEP_RED = "#D1442A"
TEXT = "#1A1A1A"
MUTED = "#666666"
RULE = "#EBEDF0"


def text(value: Any, fallback: str = "-") -> str:
    if value is None:
        return fallback
    value = str(value).strip()
    return value or fallback


def esc(value: Any, fallback: str = "-") -> str:
    return html.escape(text(value, fallback)).replace("\n", "<br>")


def slug(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")


def pill(value: Any) -> str:
    label = text(value)
    level = "neutral"
    if label in {"高", "存在差异", "不建议推进"}:
        level = "high"
    elif label in {"中", "部分一致", "有条件推进", "暂缓"}:
        level = "medium"
    elif label in {"低", "一致", "已核验", "建议继续尽调"}:
        level = "low"
    elif label in {"信息不足", "无法核验", "未取得", "未检索到", "管理人陈述", "未核验"}:
        level = "unknown"
    return f'<span class="pill {level}">{esc(label)}</span>'


def link(url: Any, label: Any | None = None) -> str:
    href = text(url, "")
    if not href:
        return "-"
    shown = text(label, href)
    if not href.startswith(("http://", "https://")):
        return esc(shown)
    return f'<a href="{html.escape(href, quote=True)}" target="_blank" rel="noopener noreferrer">{esc(shown)}</a>'


def section(title: str, number: int, body: str, section_id: str | None = None) -> str:
    identifier = section_id or f"section-{number}"
    return f'''<section id="{identifier}" class="report-section">
      <div class="section-heading"><span>{number:02d}</span><h2>{esc(title)}</h2></div>
      <div class="section-rule"></div>
      {body}
    </section>'''


def bullets(items: Iterable[Any]) -> str:
    values = list(items)
    if not values:
        return '<p class="muted">未提供</p>'
    return '<ul class="bullet-list">' + "".join(f"<li>{esc(item)}</li>" for item in values) + "</ul>"


def data_table(headers: list[str], rows: list[list[str]], classes: str = "") -> str:
    head = "".join(f"<th>{esc(item)}</th>" for item in headers)
    body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return f'<div class="table-wrap"><table class="{classes}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def key_values(items: list[tuple[str, Any]]) -> str:
    return '<div class="facts">' + "".join(
        f'<div class="fact"><dt>{esc(label)}</dt><dd>{esc(value)}</dd></div>' for label, value in items
    ) + "</div>"


def nav_svg(series: list[dict[str, Any]]) -> str:
    valid = [x for x in series if x.get("nav") is not None]
    if len(valid) < 2:
        return '<div class="empty">净值数据不足，未生成曲线</div>'
    width, height = 920, 340
    left, right, top, bottom = 74, 28, 40, 62
    plot_w, plot_h = width - left - right, height - top - bottom
    nav = [float(x["nav"]) for x in valid]
    bench = [float(x["benchmark"]) for x in valid if x.get("benchmark") is not None]
    values = nav + bench
    low, high = min(values), max(values)
    pad = (high - low) * 0.08 or 0.05
    low, high = low - pad, high + pad

    def point(i: int, value: float) -> tuple[float, float]:
        x = left + plot_w * i / max(len(valid) - 1, 1)
        y = top + plot_h * (high - value) / (high - low)
        return x, y

    grid = []
    for i in range(5):
        y = top + plot_h * i / 4
        value = high - (high - low) * i / 4
        grid.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left+plot_w}" y2="{y:.1f}" class="grid"/>')
        grid.append(f'<text x="{left-12}" y="{y+4:.1f}" text-anchor="end" class="axis">{value:.2f}</text>')

    nav_points = " ".join(f"{x:.1f},{y:.1f}" for x, y in (point(i, value) for i, value in enumerate(nav)))
    benchmark_points = []
    if bench and len(bench) == len(valid):
        benchmark_points = [point(i, float(item["benchmark"])) for i, item in enumerate(valid)]
    bench_poly = ""
    if benchmark_points:
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in benchmark_points)
        bench_poly = f'<polyline points="{pts}" class="benchmark-line"/>'

    label_indices = sorted(set(round(i * (len(valid) - 1) / 5) for i in range(6)))
    labels = "".join(
        f'<text x="{point(idx, nav[idx])[0]:.1f}" y="{height-24}" text-anchor="middle" class="axis">{esc(valid[idx].get("date"), "")}</text>'
        for idx in label_indices
    )

    running_max = -math.inf
    drawdown = []
    for value in nav:
        running_max = max(running_max, value)
        drawdown.append(value / running_max - 1)
    dd_low = min(drawdown)
    dd_text = f"最大回撤（由图示序列计算）：{dd_low:.2%}"

    return f'''<figure class="chart-card">
      <div class="chart-title"><strong>净值走势</strong><span>{esc(dd_text)}</span></div>
      <svg viewBox="0 0 {width} {height}" role="img" aria-label="产品与基准净值走势">
        {''.join(grid)}
        <line x1="{left}" y1="{top+plot_h}" x2="{left+plot_w}" y2="{top+plot_h}" class="axis-line"/>
        {bench_poly}
        <polyline points="{nav_points}" class="nav-line"/>
        {labels}
        <g transform="translate({left},18)"><line x1="0" y1="0" x2="18" y2="0" stroke="{RED}" stroke-width="4"/><text x="26" y="4" class="legend">产品/策略净值</text></g>
        <g transform="translate({left+170},18)"><line x1="0" y1="0" x2="18" y2="0" stroke="{TEXT}" stroke-width="3"/><text x="26" y="4" class="legend">基准净值</text></g>
      </svg>
    </figure>'''


CSS = r'''
:root { --red:#E8663C; --deep-red:#D1442A; --pale-red:#FFF0EB; --text:#1A1A1A; --muted:#666; --rule:#EBEDF0; --soft:#FAFBFC; }
* { box-sizing:border-box; }
html { scroll-behavior:smooth; }
body { margin:0; background:#F0F0F0; color:var(--text); font-family:"PingFang SC","Microsoft YaHei","Noto Sans CJK SC",Arial,sans-serif; line-height:1.65; }
a { color:var(--deep-red); text-decoration:none; border-bottom:1px solid rgba(168,15,24,.3); overflow-wrap:anywhere; }
a:hover { color:var(--red); }
.toolbar { position:fixed; z-index:10; right:24px; bottom:24px; display:flex; gap:10px; }
.toolbar button,.toolbar a { border:0; border-radius:4px; padding:11px 18px; color:#fff; background:var(--red); cursor:pointer; box-shadow:0 8px 24px rgba(95,0,5,.2); font:600 14px inherit; }
.toolbar a { border-bottom:0; }
.report { width:min(1120px,calc(100% - 32px)); margin:40px auto; background:#fff; box-shadow:0 18px 55px rgba(0,0,0,.08); }
.cover { min-height:780px; padding:70px 72px 54px; display:flex; flex-direction:column; position:relative; overflow:hidden; }
.brand-rule { width:94px; height:7px; background:var(--red); margin-bottom:54px; }
.eyebrow { color:var(--red); font-weight:700; letter-spacing:.16em; margin:0 0 10px; }
h1 { font-size:44px; line-height:1.22; margin:0 0 16px; max-width:780px; letter-spacing:.02em; }
.cover-subtitle { font-size:20px; color:var(--muted); margin:0; }
.cover-meta { margin-top:auto; display:grid; grid-template-columns:repeat(3,1fr); border-top:1px solid var(--rule); border-left:1px solid var(--rule); }
.cover-meta div { padding:18px; border-right:1px solid var(--rule); border-bottom:1px solid var(--rule); min-height:90px; }
.cover-meta dt { font-size:12px; color:var(--muted); margin-bottom:5px; }
.cover-meta dd { margin:0; font-weight:650; }
.cover-disclaimer { margin:24px 0 0; color:var(--muted); font-size:12px; max-width:880px; }
.content { padding:54px 72px 76px; }
.toc { display:grid; grid-template-columns:repeat(2,1fr); gap:8px 28px; margin:18px 0 0; }
.toc a { display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid var(--rule); color:var(--text); }
.toc span { color:var(--red); font-variant-numeric:tabular-nums; }
.report-section { padding:28px 0 12px; scroll-margin-top:20px; }
.section-heading { display:flex; gap:14px; align-items:baseline; }
.section-heading span { color:var(--red); font-size:14px; font-weight:800; letter-spacing:.08em; }
.section-heading h2 { font-size:26px; margin:0; }
.section-rule { width:70px; height:4px; background:var(--red); margin:11px 0 22px; }
h3 { margin:24px 0 10px; font-size:17px; }
.summary { background:var(--pale-red); border-left:5px solid var(--red); padding:20px 22px; font-size:16px; }
.route-note { border:1px solid var(--rule); border-left:5px solid var(--red); padding:14px 16px; margin:14px 0; color:var(--muted); background:#fff; }
.workpaper-banner { border:1px solid var(--red); border-left:8px solid var(--red); padding:14px 18px; margin:0 0 26px; color:var(--deep-red); background:var(--pale-red); font-weight:700; }
.metric-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:20px 0; }
.metric { border:1px solid var(--rule); background:#fff; padding:16px; min-height:95px; }
.metric strong { display:block; color:var(--red); font-size:23px; line-height:1.25; overflow-wrap:anywhere; }
.metric span { display:block; color:var(--muted); font-size:12px; margin-top:5px; }
.facts { display:grid; grid-template-columns:repeat(2,1fr); border-top:1px solid var(--rule); border-left:1px solid var(--rule); }
.fact { display:grid; grid-template-columns:115px 1fr; border-right:1px solid var(--rule); border-bottom:1px solid var(--rule); min-height:52px; }
.fact dt { background:var(--pale-red); padding:12px; font-size:12px; color:var(--deep-red); font-weight:700; }
.fact dd { margin:0; padding:12px; overflow-wrap:anywhere; }
.bullet-list { padding:0; margin:8px 0 18px; list-style:none; }
.bullet-list li { position:relative; padding:5px 0 5px 20px; }
.bullet-list li::before { content:""; width:10px; height:3px; background:var(--red); position:absolute; left:0; top:17px; }
.table-wrap { width:100%; overflow-x:auto; margin:14px 0 24px; }
table { width:100%; border-collapse:collapse; font-size:13px; }
th { background:var(--pale-red); color:var(--deep-red); text-align:left; font-weight:700; }
th,td { border:1px solid var(--rule); padding:10px 11px; vertical-align:top; overflow-wrap:anywhere; }
tbody tr:nth-child(even) { background:#FCFCFC; }
.pill { display:inline-block; border-radius:3px; padding:3px 8px; font-size:11px; font-weight:700; white-space:nowrap; background:#EEE; color:#555; }
.pill.high { background:#FFF0EB; color:#D1442A; }
.pill.medium { background:#FFF4DD; color:#9A6200; }
.pill.low { background:#E6F7F3; color:#16796D; }
.pill.unknown { background:#F0F1F3; color:#666666; }
.chart-card { border:1px solid var(--rule); margin:18px 0 24px; padding:16px; }
.chart-card svg { width:100%; height:auto; display:block; }
.chart-title { display:flex; justify-content:space-between; gap:16px; align-items:baseline; }
.chart-title span { color:var(--muted); font-size:12px; }
.grid { stroke:var(--rule); stroke-width:1; }
.axis-line { stroke:#AAA; stroke-width:1; }
.axis,.legend { fill:var(--muted); font-size:12px; font-family:Arial,"Microsoft YaHei",sans-serif; }
.nav-line,.benchmark-line { fill:none; vector-effect:non-scaling-stroke; stroke-linejoin:round; stroke-linecap:round; }
.nav-line { stroke:var(--red); stroke-width:3; }
.benchmark-line { stroke:var(--text); stroke-width:1.8; opacity:.72; }
.note { border:1px solid var(--rule); border-left:4px solid var(--red); padding:14px 16px; color:var(--muted); font-size:13px; }
.score-overview { display:grid; grid-template-columns:180px 1fr; gap:18px; border:1px solid var(--rule); margin:14px 0 20px; }
.score-total { padding:22px; background:var(--pale-red); border-right:1px solid var(--rule); }
.score-total strong { display:block; color:var(--red); font-size:38px; line-height:1.1; }
.score-total span { display:block; margin-top:6px; font-weight:700; }
.score-meta { padding:18px; display:grid; grid-template-columns:repeat(2,1fr); gap:10px 18px; align-content:center; }
.score-meta div { border-bottom:1px solid var(--rule); padding-bottom:6px; }
.score-meta b { display:block; font-size:11px; color:var(--muted); }
.timeline-table td:first-child { width:118px; color:var(--deep-red); font-weight:700; white-space:nowrap; }
.timeline-table tr.risk td:first-child { border-left:4px solid var(--red); }
.timeline-table tr.positive td:first-child { border-left:4px solid #4F6B5B; }
.timeline-table tr.neutral td:first-child { border-left:4px solid #999; }
.muted,.empty { color:var(--muted); }
.footer { margin-top:46px; border-top:1px solid var(--rule); padding-top:18px; color:var(--muted); font-size:12px; }
@media (max-width:760px) {
  .report { width:100%; margin:0; box-shadow:none; }
  .cover,.content { padding:36px 22px; }
  h1 { font-size:34px; }
  .cover-meta,.facts,.metric-grid,.toc { grid-template-columns:1fr; }
  .score-overview { grid-template-columns:1fr; }
  .score-total { border-right:0; border-bottom:1px solid var(--rule); }
  .score-meta { grid-template-columns:1fr; }
  .fact { grid-template-columns:100px 1fr; }
  .toolbar { right:14px; bottom:14px; }
}
@page { size:A4; margin:14mm; }
@media print {
  body { background:#fff; font-size:9.5pt; }
  .toolbar { display:none!important; }
  .report { width:auto; margin:0; box-shadow:none; }
  .cover { min-height:260mm; padding:8mm 2mm; break-after:page; }
  .content { padding:0; }
  .toc { break-after:page; }
  .report-section { padding-top:7mm; }
  .section-heading h2 { font-size:17pt; }
  .summary,.metric,.fact,.chart-card,.note,table { break-inside:avoid; }
  .table-wrap { overflow:visible; }
  table { font-size:8pt; }
  th,td { padding:6px; }
  a { color:inherit; border:0; }
}
'''


def validate_payload(data: dict[str, Any]) -> None:
    object_keys = {
        "meta", "executive_summary", "scorecard", "company", "governance",
        "strategy", "product_universe", "performance", "conclusion", "generation_audit",
    }
    list_keys = {
        "timeline", "shareholders", "team", "products", "contradictions",
        "risk_review", "external_cross_checks", "operations", "gaps",
        "interview_questions", "monitoring_triggers", "mcp_gap_map", "evidence",
        "limitations", "report_disclosures", "product_deep_dive_queue",
    }
    for key in object_keys:
        if key in data and not isinstance(data[key], dict):
            raise ValueError(f"{key} must be an object")
    for key in list_keys:
        if key in data and not isinstance(data[key], list):
            raise ValueError(f"{key} must be an array")
    meta = data.get("meta", {})
    if not text(meta.get("manager_name"), ""):
        raise ValueError("meta.manager_name is required")
    mode = text(meta.get("report_mode"), "strategy").strip().lower()
    if mode not in {"strategy", "institutional", "full", "机构级", "机构级尽调", "准入尽调", "运营尽调", "合规尽调"}:
        raise ValueError("meta.report_mode must be strategy or institutional")
    nav_series = data.get("performance", {}).get("nav_series", [])
    if not isinstance(nav_series, list):
        raise ValueError("performance.nav_series must be an array")
    for index, item in enumerate(nav_series):
        if not isinstance(item, dict):
            raise ValueError(f"performance.nav_series[{index}] must be an object")
        if not text(item.get("date"), ""):
            raise ValueError(f"performance.nav_series[{index}].date is required")
        try:
            float(item.get("nav"))
            if item.get("benchmark") is not None:
                float(item["benchmark"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"performance.nav_series[{index}] contains a non-numeric value") from exc


def build_html(data: dict[str, Any], profile: str = "submission") -> str:
    if profile not in {"submission", "workpaper"}:
        raise ValueError("profile must be submission or workpaper")
    is_workpaper = profile == "workpaper"
    meta = data.get("meta", {})
    report_mode = text(meta.get("report_mode"), "strategy").strip().lower()
    institutional_modes = {"institutional", "full", "机构级", "机构级尽调", "准入尽调", "运营尽调", "合规尽调"}
    show_institutional_detail = is_workpaper or report_mode in institutional_modes
    manager = text(meta.get("manager_name"), "")
    if not manager:
        raise ValueError("meta.manager_name is required")
    title = text(meta.get("title"), "火富牛-私募基金管理人尽调报告")
    subtitle = text(meta.get("subtitle"), "管理人及投资策略评估")
    report_date = text(meta.get("report_date"), str(date.today()))

    sections: list[tuple[str, str]] = []
    number = 1
    executive = data.get("executive_summary", {})
    metrics = [
        (executive.get("overall_view", "待评估"), "总体意见"),
        (executive.get("evidence_completeness", meta.get("evidence_completeness", "待评估")), "证据完整度"),
        (executive.get("top_risk", "信息不足"), "最高风险"),
    ]
    body = f'<div class="summary">{esc(executive.get("summary", "未提供尽调摘要"))}</div>'
    if is_workpaper and data.get("route_notice"):
        body += f'<div class="route-note"><strong>信息路径：</strong>{esc(data["route_notice"])}</div>'
    body += '<div class="metric-grid">' + "".join(f'<div class="metric"><strong>{esc(v)}</strong><span>{esc(k)}</span></div>' for v, k in metrics) + "</div>"
    if executive.get("key_observations"):
        body += "<h3>核心观察</h3>" + bullets(executive["key_observations"])
    sections.append(("尽调摘要", section("尽调摘要", number, body))); number += 1

    audit = data.get("generation_audit", {})
    if is_workpaper and (audit or meta.get("data_route")):
        body = key_values([
            ("信息路径", audit.get("route", meta.get("data_route", "未注明"))),
            ("检索档位", audit.get("retrieval_profile", "标准尽调")),
            ("调用预算", audit.get("planned_call_budget", "未注明")),
            ("实际调用", audit.get("actual_call_count", "未记录")),
            ("采集方式", audit.get("collection_mode", "未注明")),
            ("生成时间", audit.get("generated_at", report_date)),
            ("来源覆盖", audit.get("source_coverage", "见证据台账")),
            ("工具可用性", audit.get("tool_availability", "未注明")),
            ("复核状态", audit.get("review_status", "待人工复核")),
        ])
        tool_runs = audit.get("tool_runs", [])
        if tool_runs:
            body += "<h3>工具调用与查询结果</h3>" + data_table(
                ["工具/来源", "查询范围", "结果", "时间", "问题/限制"],
                [[esc(x.get("name")), esc(x.get("scope")), esc(x.get("result")), esc(x.get("time")), esc(x.get("issue"))] for x in tool_runs],
            )
        calculations = audit.get("calculations", [])
        if calculations:
            body += "<h3>衍生计算口径</h3>" + data_table(
                ["指标", "输入数据", "方法", "复核状态"],
                [[esc(x.get("metric")), esc(x.get("inputs")), esc(x.get("method")), pill(x.get("status"))] for x in calculations],
            )
        issues = audit.get("unresolved_issues", [])
        if issues:
            body += "<h3>生成过程未解决事项</h3>" + bullets(issues)
        skipped_calls = audit.get("skipped_calls", [])
        if skipped_calls:
            body += "<h3>已跳过的高成本查询</h3>" + data_table(
                ["对象/查询", "跳过原因", "后续安排"],
                [[esc(x.get("item")), esc(x.get("reason")), esc(x.get("next_step"))] for x in skipped_calls],
            )
        deep_dive_queue = data.get("product_deep_dive_queue", [])
        if deep_dive_queue:
            body += "<h3>产品业绩深挖队列</h3>"
            body += '<p class="note">以下任务未纳入本次管理人尽调的默认调用预算，可交由产品业绩专项任务继续处理。</p>'
            body += data_table(
                ["优先级", "产品", "产品代码", "策略", "入队原因", "建议核验"],
                [[
                    pill(x.get("priority")),
                    esc(x.get("product_name")),
                    esc(x.get("product_code")),
                    esc(x.get("strategy")),
                    esc(x.get("selection_reason")),
                    esc(x.get("needed_checks")),
                ] for x in deep_dive_queue],
            )
        body += '<p class="note">本节仅用于研究人员复核，不随正式报告提交。</p>'
        sections.append(("编制与数据审计", section("编制与数据审计", number, body))); number += 1

    scorecard = data.get("scorecard", {})
    if scorecard and (show_institutional_detail or meta.get("show_scorecard") is True):
        total = scorecard.get("total", "暂不评分")
        maximum = scorecard.get("max_score", 100)
        score_display = f"{esc(total)}/{esc(maximum)}" if str(total).replace(".", "", 1).isdigit() else esc(total)
        body = f'''<div class="score-overview">
          <div class="score-total"><strong>{score_display}</strong><span>{esc(scorecard.get("rating", "待评估"))}</span></div>
          <div class="score-meta">
            <div><b>总体置信度</b>{esc(scorecard.get("confidence", "不足"))}</div>
            <div><b>评分用途</b>{esc(scorecard.get("purpose", "综合评估"))}</div>
            <div><b>评级区间</b>{esc(scorecard.get("bands", "85-100 优质；70-84 合格；55-69 存疑；<55 规避"))}</div>
            <div><b>覆盖说明</b>{esc(scorecard.get("coverage_note", "见各维度证据与置信度"))}</div>
          </div>
        </div>'''
        dimensions = scorecard.get("dimensions", [])
        if dimensions:
            rows = [[
                esc(x.get("name")),
                esc(f'{x.get("score", "暂不评分")}/{x.get("max_score", 20)}' if x.get("score") is not None else "暂不评分"),
                esc(x.get("positive_evidence")),
                esc(x.get("risk_evidence")),
                pill(x.get("confidence")),
            ] for x in dimensions]
            body += data_table(["维度", "得分", "正向依据", "风险/反证", "置信度"], rows)
        score_note = "评分仅用于内部研究摘要；重大监管事项、身份冲突或关键数据缺口可以覆盖数值结论。" if is_workpaper else "评分用于结构化辅助判断；重大监管事项、身份冲突或关键数据缺口可以覆盖数值结论。"
        body += f'<p class="note">{score_note}</p>'
        sections.append(("健康度评分卡", section("健康度评分卡", number, body))); number += 1

    timeline = data.get("timeline", [])
    if timeline:
        rows = []
        for x in timeline:
            row_class = text(x.get("type"), "neutral")
            detail = esc(x.get("event"))
            if x.get("detail"):
                detail += f'<br><span class="muted">{esc(x.get("detail"))}</span>'
            if show_institutional_detail and x.get("source"):
                detail += f'<br><span class="muted">来源：{esc(x.get("source"))}</span>'
            status_cell = f'<td>{pill(x.get("status", "已核验"))}</td>' if show_institutional_detail else ""
            rows.append(f'<tr class="{html.escape(row_class, quote=True)}"><td>{esc(x.get("date"))}</td><td>{detail}</td>{status_cell}</tr>')
        status_header = "<th>证据状态</th>" if show_institutional_detail else ""
        body = f'<div class="table-wrap"><table class="timeline-table"><thead><tr><th>日期</th><th>事件与含义</th>{status_header}</tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>"
        sections.append(("关键事件时间轴", section("关键事件时间轴", number, body))); number += 1

    company = data.get("company", {})
    if company:
        pairs = [
            ("公司名称", company.get("legal_name")), ("登记编号", company.get("registration_number")),
            ("成立时间", company.get("founded_date")), ("登记时间", company.get("registration_date")),
            ("法定代表人", company.get("legal_representative")), ("管理人类型", company.get("manager_type")),
            ("管理规模", company.get("management_scale")), ("运作产品数", company.get("active_products")),
            ("注册地址", company.get("registered_address")), ("办公地址", company.get("office_address")),
            ("当前状态", company.get("status")),
        ]
        if show_institutional_detail:
            pairs.append(("主要来源", company.get("data_source")))
        body = key_values(pairs)
        company_note = company.get("notes") if show_institutional_detail else company.get("submission_note")
        if company_note:
            body += f'<p class="note">{esc(company_note)}</p>'
        sections.append(("管理人基本信息", section("管理人基本信息", number, body))); number += 1

    shareholders = data.get("shareholders", [])
    governance = data.get("governance", {})
    if shareholders or governance:
        if show_institutional_detail:
            rows = [[esc(x.get("name")), esc(x.get("type")), esc(x.get("ownership")), esc(x.get("subscribed_capital")), pill(x.get("status"))] for x in shareholders]
            body = data_table(["股东名称", "股东类型", "持股比例", "认缴出资", "证据状态"], rows) if rows else ""
        else:
            rows = [[esc(x.get("name")), esc(x.get("type")), esc(x.get("ownership"))] for x in shareholders]
            body = data_table(["股东名称", "股东类型", "持股比例"], rows) if rows else ""
        if governance:
            governance_pairs = [("实际控制人", governance.get("actual_controller"))]
            if show_institutional_detail:
                governance_pairs.extend([
                    ("治理与授权", governance.get("structure")),
                    ("关联关系与利益冲突", governance.get("conflicts")),
                    ("待核实事项", governance.get("open_items")),
                ])
            body += key_values(governance_pairs)
        sections.append(("股权与治理", section("股权与治理", number, body))); number += 1

    team = data.get("team", [])
    if team:
        if show_institutional_detail:
            rows = [[esc(x.get("name")), esc(x.get("role")), esc(x.get("background")), esc(x.get("key_person_risk")), pill(x.get("status"))] for x in team]
            body = data_table(["姓名", "角色", "履历与职责", "稳定性/关键人风险", "证据状态"], rows)
        else:
            rows = [[esc(x.get("name")), esc(x.get("role")), esc(x.get("background"))] for x in team]
            body = data_table(["姓名", "角色", "履历与策略分工"], rows)
        sections.append(("团队情况", section("团队情况", number, body))); number += 1

    strategy = data.get("strategy", {})
    if strategy:
        body = f'<div class="summary"><strong>策略类型：</strong>{esc(strategy.get("type"))}<br>{esc(strategy.get("overview"))}</div>'
        dims = strategy.get("dimensions", [])
        if dims:
            if show_institutional_detail:
                rows = [[esc(x.get("name")), esc(x.get("detail")), pill(x.get("status"))] for x in dims]
                body += data_table(["维度", "尽调内容", "证据状态"], rows)
            else:
                rows = [[esc(x.get("name")), esc(x.get("detail"))] for x in dims]
                body += data_table(["策略维度", "核心要点"], rows)
        sections.append(("投资策略与流程", section("投资策略与流程", number, body))); number += 1

    universe = data.get("product_universe", {})
    if universe:
        overview_metrics = [
            (universe.get("total_filed", "-"), "全部备案产品"),
            (universe.get("active", "-"), "运作中"),
            (universe.get("early_liquidated", "-"), "提前清算"),
            (universe.get("nav_coverage", "-"), "净值覆盖率"),
        ]
        body = '<div class="metric-grid">' + "".join(f'<div class="metric"><strong>{esc(v)}</strong><span>{esc(k)}</span></div>' for v, k in overview_metrics) + "</div>"
        if universe.get("scope_note"):
            body += f'<p class="note">{esc(universe.get("scope_note"))}</p>'
        states = universe.get("status_distribution", [])
        if states:
            body += "<h3>运作状态分布</h3>" + data_table(
                ["状态", "数量", "占比", "说明"],
                [[esc(x.get("name")), esc(x.get("count")), esc(x.get("share")), esc(x.get("note"))] for x in states],
            )
        strategies = universe.get("strategy_distribution", [])
        if strategies:
            body += "<h3>策略分布</h3>" + data_table(
                ["策略", "数量", "占比", "说明"],
                [[esc(x.get("name")), esc(x.get("count")), esc(x.get("share")), esc(x.get("note"))] for x in strategies],
            )
        if universe.get("analysis"):
            body += f'<p>{esc(universe.get("analysis"))}</p>'
        sections.append(("产品全景与规模变迁", section("产品全景与规模变迁", number, body))); number += 1

    products = data.get("products", [])
    performance = data.get("performance", {})
    if products or performance:
        body = ""
        if products:
            rows = [[esc(x.get("name")), esc(x.get("strategy")), esc(x.get("inception")), esc(x.get("status")), esc(x.get("nav_end_date")), esc(x.get("note"))] for x in products]
            body += data_table(["产品名称", "策略", "成立日期", "状态", "净值截止", "代表性/备注"], rows)
        if performance:
            if performance.get("basis_note"):
                body += f'<p class="note"><strong>业绩口径：</strong>{esc(performance["basis_note"])}</p>'
            items = performance.get("metrics", [])
            if items:
                body += '<div class="metric-grid">' + "".join(f'<div class="metric"><strong>{esc(x.get("value"))}</strong><span>{esc(x.get("label"))}</span></div>' for x in items) + "</div>"
            body += nav_svg(performance.get("nav_series", []))
            annual = performance.get("annual_returns", [])
            if annual:
                body += "<h3>年度收益与对照</h3>" + data_table(
                    ["年度/区间", "管理人/产品", "基准", "同策略参考", "说明"],
                    [[esc(x.get("period")), esc(x.get("manager")), esc(x.get("benchmark")), esc(x.get("peer")), esc(x.get("note"))] for x in annual],
                )
            rolling = performance.get("rolling_returns", [])
            if rolling:
                body += "<h3>滚动区间收益</h3>" + data_table(
                    ["区间", "管理人/产品", "基准", "同策略参考", "结论"],
                    [[esc(x.get("period")), esc(x.get("manager")), esc(x.get("benchmark")), esc(x.get("peer")), esc(x.get("conclusion"))] for x in rolling],
                )
            peers = performance.get("peer_comparison", [])
            if peers:
                body += "<h3>同策略横向对照</h3>" + data_table(
                    ["周期", "管理人/产品", "同策略中位数", "同策略均值/分位", "结论"],
                    [[esc(x.get("period")), esc(x.get("manager")), esc(x.get("median")), esc(x.get("mean_or_percentile")), esc(x.get("conclusion"))] for x in peers],
                )
            if performance.get("analysis"):
                body += f'<p>{esc(performance["analysis"])}</p>'
        sections.append(("产品与业绩", section("产品与业绩", number, body))); number += 1

    contradictions = data.get("contradictions", [])
    if contradictions and show_institutional_detail:
        rows = [[
            esc(x.get("claim")), esc(x.get("fact")), pill(x.get("assessment")),
            esc(x.get("source")), esc(x.get("note")),
        ] for x in contradictions]
        body = data_table(["公开表述/主张", "可核实事实", "判定", "来源", "边界/说明"], rows)
        sections.append(("言行一致性核验", section("言行一致性核验", number, body))); number += 1

    risks = data.get("risk_review", [])
    visible_risks = risks if show_institutional_detail else [
        x for x in risks
        if x.get("include_in_strategy") is True
        or (
            text(x.get("level")) != "信息不足"
            and ("运营" not in text(x.get("dimension")) or text(x.get("level")) == "高")
        )
    ]
    if visible_risks:
        if show_institutional_detail:
            has_boundary = any(x.get("boundary") for x in visible_risks)
            rows = []
            for x in visible_risks:
                row = [esc(x.get("dimension")), esc(x.get("finding")), pill(x.get("level")), esc(x.get("basis"))]
                if has_boundary:
                    row.append(esc(x.get("boundary")))
                row.append(esc(x.get("action")))
                rows.append(row)
            headers = ["维度", "发现", "等级", "依据/置信度"] + (["反证/边界"] if has_boundary else []) + ["建议动作"]
        else:
            rows = [[esc(x.get("dimension")), esc(x.get("finding")), pill(x.get("level"))] for x in visible_risks]
            headers = ["风险点", "主要判断", "等级"]
        body = data_table(headers, rows)
        risk_title = "风险、合规与舆情" if show_institutional_detail else "主要风险观察"
        sections.append((risk_title, section(risk_title, number, body))); number += 1

    checks = data.get("external_cross_checks", [])
    if checks and show_institutional_detail:
        rows = []
        for x in checks:
            platform = link(x.get("url"), x.get("platform")) if x.get("url") else esc(x.get("platform"))
            rows.append([platform, esc(x.get("item")), esc(x.get("result")), esc(x.get("date")), pill(x.get("status")), esc(x.get("note"))])
        body = '<p class="note">商业平台数据仅作补充交叉验证，不替代协会、监管机构、托管/估值或管理人正式材料。</p>'
        body += data_table(["平台/来源", "核验事项", "展示结果", "日期", "一致性", "差异/限制"], rows)
        sections.append(("外部平台交叉核验", section("外部平台交叉核验", number, body))); number += 1

    operations = data.get("operations", [])
    if operations and show_institutional_detail:
        rows = [[esc(x.get("dimension")), esc(x.get("finding")), pill(x.get("status")), esc(x.get("action"))] for x in operations]
        body = data_table(["模块", "现状/发现", "证据状态", "待办"], rows)
        sections.append(("运营尽调", section("运营尽调", number, body))); number += 1

    gaps = data.get("gaps", [])
    questions = data.get("interview_questions", [])
    if is_workpaper and (gaps or questions):
        body = ""
        if gaps:
            body += "<h3>优先补充资料</h3>" + bullets(gaps)
        if questions:
            body += "<h3>管理人访谈问题</h3>" + bullets([f"{i}. {q}" for i, q in enumerate(questions, 1)])
        sections.append(("数据缺口与访谈问题", section("数据缺口与访谈问题", number, body))); number += 1

    conclusion = data.get("conclusion", {})
    if conclusion:
        body = f'<div class="summary"><strong>总体意见：</strong>{esc(conclusion.get("view", "待评估"))}<br>{esc(conclusion.get("rationale"))}</div>'
        if show_institutional_detail and conclusion.get("conditions"):
            body += "<h3>前置条件</h3>" + bullets(conclusion["conditions"])
        if not show_institutional_detail and conclusion.get("boundaries"):
            body += "<h3>判断边界</h3>" + bullets(conclusion["boundaries"])
        if show_institutional_detail and conclusion.get("monitoring"):
            body += "<h3>持续跟踪</h3>" + bullets(conclusion["monitoring"])
        conclusion_title = "结论与后续安排" if show_institutional_detail else "综合判断"
        sections.append((conclusion_title, section(conclusion_title, number, body))); number += 1

    monitoring = data.get("monitoring_triggers", [])
    gap_map = data.get("mcp_gap_map", [])
    if (monitoring and show_institutional_detail) or (is_workpaper and gap_map):
        body = ""
        if monitoring:
            body += "<h3>触发式监测清单</h3>" + data_table(
                ["监测项", "触发条件", "频率/优先级", "重新评估动作"],
                [[esc(x.get("item")), esc(x.get("trigger")), esc(x.get("frequency_or_priority")), esc(x.get("action"))] for x in monitoring],
            )
        if is_workpaper and gap_map:
            body += "<h3>火富牛 MCP 数据缺口与补充项</h3>"
            body += '<p class="note">该表记录未连接、已调用但未返回、权限受限或现有工具不能覆盖的数据，以及进一步补充后可支持的判断。缺失数据不等于负面事实。</p>'
            body += data_table(
                ["缺失数据", "对应工具", "补齐后的用途", "当前影响"],
                [[esc(x.get("gap")), esc(x.get("tool")), esc(x.get("decision_value")), esc(x.get("current_impact"))] for x in gap_map],
            )
        monitoring_title = "监测清单与数据缺口" if is_workpaper else "持续监测安排"
        sections.append((monitoring_title, section(monitoring_title, number, body))); number += 1

    evidence = data.get("evidence", [])
    if is_workpaper and evidence:
        rows = []
        for x in evidence:
            source = esc(x.get("source"))
            if x.get("url"):
                source += "<br>" + link(x.get("url"), "查看来源")
            rows.append([esc(x.get("id")), esc(x.get("fact")), source, esc(x.get("date")), pill(x.get("status")), esc(x.get("limitation"))])
        body = data_table(["ID", "事项与事实", "来源", "日期", "状态", "限制/备注"], rows)
        sections.append(("证据台账", section("证据台账", number, body))); number += 1

    limitations = data.get("limitations", []) if is_workpaper else data.get("report_disclosures", [])
    if limitations:
        body = bullets(limitations)
        sections.append(("范围限制与声明", section("范围限制与声明", number, body))); number += 1

    toc = '<nav class="toc">' + "".join(f'<a href="#section-{idx}"><span>{idx:02d}</span>{esc(title_)}</a>' for idx, (title_, _) in enumerate(sections, 1)) + "</nav>"
    if is_workpaper:
        cover_meta = [
            ("报告用途", meta.get("purpose", "管理人尽职调查")),
            ("报告日期", report_date),
            ("数据截止", meta.get("data_cutoff", "未注明")),
            ("信息路径", meta.get("data_route", "未注明")),
            ("证据完整度", meta.get("evidence_completeness", "待评估")),
            ("版本", "研究工作底稿"),
        ]
    else:
        cover_meta = [
            ("报告用途", meta.get("purpose", "管理人尽职调查")),
            ("报告日期", report_date),
            ("数据截止", meta.get("data_cutoff", "未注明")),
            ("编制主体", meta.get("author", "火富牛尽调助手")),
            ("登记编号", data.get("company", {}).get("registration_number", "未注明")),
            ("保密级别", meta.get("confidentiality", "内部参考")),
        ]
    cover_meta_html = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in cover_meta)
    disclaimer = text(meta.get("disclaimer"), "本报告基于截至数据截止日可获得的资料编制。私募管理人公开披露可能有限，未取得或未经独立验证的信息不应被视为已确认事实。本报告仅供尽职调查参考，不构成投资建议、法律意见或审计鉴证。")
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="{html.escape(manager, quote=True)}火富牛私募基金管理人尽调报告">
  <title>{esc(manager)}｜{esc(title)}{'｜研究工作底稿' if is_workpaper else ''}</title>
  <style>{CSS}</style>
</head>
<body>
  <div class="toolbar"><a href="#top">返回顶部</a><button type="button" onclick="window.print()">打印报告</button></div>
  <main id="top" class="report">
    <header class="cover">
      <div class="brand-rule"></div>
      <p class="eyebrow">FOF99 · PRIVATE FUND MANAGER DUE DILIGENCE</p>
      <h1>{esc(title)}</h1>
      <p class="cover-subtitle">{esc(manager)}｜{esc(subtitle)}</p>
      <dl class="cover-meta">{cover_meta_html}</dl>
      <p class="cover-disclaimer">{esc(disclaimer)}</p>
    </header>
    <div class="content">
      {'<div class="workpaper-banner">研究工作底稿｜记录数据路径、来源覆盖与生成问题，不随正式报告提交</div>' if is_workpaper else ''}
      <section><div class="section-heading"><span>目录</span><h2>报告导航</h2></div><div class="section-rule"></div>{toc}</section>
      {''.join(content for _, content in sections)}
      <footer class="footer">数据截止：{esc(meta.get("data_cutoff", "未注明"))}｜报告日期：{esc(report_date)}<br>仅供尽职调查参考，不构成投资建议、法律意见或审计鉴证。</footer>
    </div>
  </main>
</body>
</html>'''


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="UTF-8 JSON report data")
    parser.add_argument("--output", required=True, help="Output HTML path")
    parser.add_argument("--workpaper-output", help="Internal workpaper HTML path; defaults beside the report")
    parser.add_argument("--no-workpaper", action="store_true", help="Do not generate the internal workpaper")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    if input_path == output_path:
        raise ValueError("Input and output paths must differ")
    with input_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("Top-level JSON value must be an object")
    validate_payload(payload)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_html(payload, profile="submission"), encoding="utf-8")
    if output_path.stat().st_size < 1024:
        raise RuntimeError("HTML generation failed or produced an empty file")
    print(str(output_path))
    if not args.no_workpaper:
        workpaper_path = (
            Path(args.workpaper_output).expanduser().resolve()
            if args.workpaper_output
            else output_path.with_name(f"{output_path.stem}-workpaper{output_path.suffix}")
        )
        if workpaper_path in {input_path, output_path}:
            raise ValueError("Workpaper path must differ from input and report paths")
        workpaper_path.parent.mkdir(parents=True, exist_ok=True)
        workpaper_path.write_text(build_html(payload, profile="workpaper"), encoding="utf-8")
        if workpaper_path.stat().st_size < 1024:
            raise RuntimeError("Workpaper generation failed or produced an empty file")
        print(str(workpaper_path))


if __name__ == "__main__":
    main()

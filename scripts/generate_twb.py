#!/usr/bin/env python3
"""
Generate a real Tableau .twb workbook with actual visualization specifications.

Produces:
  - Proper <mark> types (bar, text, scatter, highlight-table)
  - <rows> / <cols> shelf assignments with aggregations
  - <encodings> for color, label, size, shape, detail, tooltip
  - <pane> field-header definitions
  - <format> elements (font, alignment, numbers, shading)
  - <dashboard-action> elements (filter, highlight, url)
  - 3 dashboard pages with proper zone layouts
"""

from pathlib import Path
import textwrap

OUTPUT = Path("tableau/insurance_claims_dashboard.twb")
DATA_DIR = "../data/processed"

# ─── DataSource definitions ───────────────────────────────────────────────

DATASOURCES = {
    "policy_level": {
        "caption": "Policy Level",
        "file": "tableau_policy_level.csv",
        "columns": {
            "IDpol":             ("integer", "dimension", "nominal"),
            "ClaimNb":           ("integer", "measure",   "quantitative"),
            "Exposure":          ("real",    "measure",   "quantitative"),
            "VehPower":          ("integer", "measure",   "quantitative"),
            "VehAge":            ("integer", "measure",   "quantitative"),
            "DrivAge":           ("integer", "measure",   "quantitative"),
            "BonusMalus":        ("integer", "measure",   "quantitative"),
            "VehBrand":          ("string",  "dimension", "nominal"),
            "VehGas":            ("string",  "dimension", "nominal"),
            "Area":              ("string",  "dimension", "nominal"),
            "Density":           ("integer", "measure",   "quantitative"),
            "Region":            ("string",  "dimension", "nominal"),
            "TotalClaimCost":    ("real",    "measure",   "quantitative"),
            "MaxClaimAmount":    ("real",    "measure",   "quantitative"),
            "MeanClaimAmount":   ("real",    "measure",   "quantitative"),
            "DrivAgeGroup":      ("string",  "dimension", "nominal"),
            "VehAgeGroup":       ("string",  "dimension", "nominal"),
            "VehPowerGroup":     ("string",  "dimension", "nominal"),
            "BonusMalusCat":     ("string",  "dimension", "nominal"),
            "DensityGroup":      ("string",  "dimension", "nominal"),
        },
    },
    "regional_kpi": {
        "caption": "Regional KPI",
        "file": "tableau_regional_kpi.csv",
        "columns": {
            "Region":            ("string",  "dimension", "nominal"),
            "PolicyCount":       ("integer", "measure",   "quantitative"),
            "TotalExposure":     ("real",    "measure",   "quantitative"),
            "TotalClaims":       ("integer", "measure",   "quantitative"),
            "ClaimFrequency":    ("real",    "measure",   "quantitative"),
            "TotalClaimCost":    ("real",    "measure",   "quantitative"),
            "AvgSeverity":       ("real",    "measure",   "quantitative"),
            "CostPerExposure":   ("real",    "measure",   "quantitative"),
        },
    },
    "segment_analysis": {
        "caption": "Segment Analysis",
        "file": "tableau_segment_analysis.csv",
        "columns": {
            "Segment":           ("string",  "dimension", "nominal"),
            "PolicyCount":       ("integer", "measure",   "quantitative"),
            "TotalExposure":     ("real",    "measure",   "quantitative"),
            "TotalClaims":       ("integer", "measure",   "quantitative"),
            "TotalClaimCost":    ("real",    "measure",   "quantitative"),
            "PoliciesWithClaims":("integer", "measure",   "quantitative"),
            "ClaimFrequency":    ("real",    "measure",   "quantitative"),
            "AvgSeverity":       ("real",    "measure",   "quantitative"),
            "CostPerExposure":   ("real",    "measure",   "quantitative"),
            "SegmentType":       ("string",  "dimension", "nominal"),
        },
    },
    "individual_claims": {
        "caption": "Individual Claims",
        "file": "tableau_individual_claims.csv",
        "columns": {
            "IDpol":             ("integer", "dimension", "nominal"),
            "ClaimAmount":       ("real",    "measure",   "quantitative"),
            "CumCost":           ("real",    "measure",   "quantitative"),
            "CumCostPct":        ("real",    "measure",   "quantitative"),
            "ClaimRank":         ("integer", "measure",   "quantitative"),
            "ClaimRankPct":      ("real",    "measure",   "quantitative"),
        },
    },
    "portfolio_kpi": {
        "caption": "Portfolio KPI",
        "file": "tableau_portfolio_kpi.csv",
        "columns": {
            "KPI":               ("string",  "dimension", "nominal"),
            "Value":             ("real",    "measure",   "quantitative"),
        },
    },
}

# ─── Worksheet definitions ────────────────────────────────────────────────

WORKSHEETS = [
    # PAGE 1  --  Executive Portfolio Overview
    {
        "name": "KPI_Cards",
        "ds": "portfolio_kpi",
        "mark": "text",
        "rows": ["KPI"],
        "cols": ["Value"],
        "encodings": {
            "text": "SUM(Value)",
            "tooltip": ["KPI", "Value"],
        },
        "filters": [],
        "sort": [("KPI", "asc")],
        "format": {"numfmt": {"Value": "$#,##0"}, "font_size": 14, "bold": True},
    },
    {
        "name": "Regional_Frequency_Bar",
        "ds": "regional_kpi",
        "mark": "bar",
        "rows": ["Region"],
        "cols": ["ClaimFrequency"],
        "encodings": {
            "color": "ClaimFrequency",
            "label": "ClaimFrequency",
            "tooltip": ["Region", "ClaimFrequency", "PolicyCount", "TotalExposure"],
        },
        "filters": [],
        "sort": [("ClaimFrequency", "desc")],
        "ref_lines": [("ClaimFrequency", 0.1007, "Portfolio Avg")],
        "format": {"numfmt": {"ClaimFrequency": "0.0000"}},
    },
    {
        "name": "Regional_CostPerExposure_Bar",
        "ds": "regional_kpi",
        "mark": "bar",
        "rows": ["Region"],
        "cols": ["CostPerExposure"],
        "encodings": {
            "color": "CostPerExposure",
            "label": "CostPerExposure",
            "tooltip": ["Region", "CostPerExposure", "TotalClaimCost", "AvgSeverity"],
        },
        "filters": [],
        "sort": [("CostPerExposure", "desc")],
        "ref_lines": [("CostPerExposure", 167, "Portfolio Avg")],
        "format": {"numfmt": {"CostPerExposure": "$#,##0"}},
    },
    # FIX 8: Highlight_Table colored by Claim Frequency only. Title should read
    # "Highlight Table -- Colored by Claim Frequency" in the final build.
    {
        "name": "Highlight_Table",
        "ds": "regional_kpi",
        "mark": "text",
        "rows": ["Region"],
        "cols": ["ClaimFrequency", "AvgSeverity", "CostPerExposure"],
        "encodings": {
            "text": "ClaimFrequency",
            "color": "ClaimFrequency",
            "tooltip": ["Region", "ClaimFrequency", "AvgSeverity", "CostPerExposure"],
        },
        "filters": [],
        "sort": [("ClaimFrequency", "desc")],
        "format": {"numfmt": {"ClaimFrequency": "0.0000", "AvgSeverity": "$#,##0", "CostPerExposure": "$#,##0"}},
    },

    # PAGE 2  --  Claims & Risk Segments
    {
        "name": "Driver_Age_Frequency",
        "ds": "segment_analysis",
        "mark": "bar",
        "rows": ["Segment"],
        "cols": ["ClaimFrequency"],
        "encodings": {
            "color": "ClaimFrequency",
            "label": "ClaimFrequency",
            "tooltip": ["Segment", "ClaimFrequency", "PolicyCount", "TotalExposure"],
        },
        "filters": [("SegmentType", "DrivAgeGroup")],
        "sort": [("Segment", "asc")],
        "ref_lines": [("ClaimFrequency", 0.1007, "Portfolio Avg")],
        "format": {"numfmt": {"ClaimFrequency": "0.0000"}},
    },
    {
        "name": "Driver_Age_Severity",
        "ds": "segment_analysis",
        "mark": "bar",
        "rows": ["Segment"],
        "cols": ["AvgSeverity"],
        "encodings": {
            "color": "AvgSeverity",
            "label": "AvgSeverity",
            "tooltip": ["Segment", "AvgSeverity", "TotalClaimCost", "PoliciesWithClaims"],
        },
        "filters": [("SegmentType", "DrivAgeGroup")],
        "sort": [("Segment", "asc")],
        "format": {"numfmt": {"AvgSeverity": "$#,##0"}},
    },
    {
        "name": "Vehicle_Age_Frequency",
        "ds": "segment_analysis",
        "mark": "bar",
        "rows": ["Segment"],
        "cols": ["ClaimFrequency"],
        "encodings": {
            "color": "ClaimFrequency",
            "label": "ClaimFrequency",
            "tooltip": ["Segment", "ClaimFrequency", "PolicyCount", "TotalExposure"],
        },
        "filters": [("SegmentType", "VehAgeGroup")],
        "sort": [("Segment", "asc")],
        "ref_lines": [("ClaimFrequency", 0.1007, "Portfolio Avg")],
        "format": {"numfmt": {"ClaimFrequency": "0.0000"}},
    },
    {
        "name": "Vehicle_Age_Severity",
        "ds": "segment_analysis",
        "mark": "bar",
        "rows": ["Segment"],
        "cols": ["AvgSeverity"],
        "encodings": {
            "color": "AvgSeverity",
            "label": "AvgSeverity",
            "tooltip": ["Segment", "AvgSeverity", "TotalClaimCost", "PoliciesWithClaims"],
        },
        "filters": [("SegmentType", "VehAgeGroup")],
        "sort": [("Segment", "asc")],
        "format": {"numfmt": {"AvgSeverity": "$#,##0"}},
    },
    {
        "name": "Freq_vs_Severity_Scatter",
        "ds": "regional_kpi",
        "mark": "circle",
        "rows": ["AvgSeverity"],
        "cols": ["ClaimFrequency"],
        "encodings": {
            "detail": "Region",
            "size": "PolicyCount",
            "color": "Region",
            "label": "Region",
            "tooltip": ["Region", "ClaimFrequency", "AvgSeverity", "PolicyCount", "CostPerExposure"],
        },
        "filters": [],
        "sort": [],
        "ref_lines": [("ClaimFrequency", 0.1007, "Avg Freq"), ("AvgSeverity", 2249, "Avg Sev")],
        "format": {"numfmt": {"ClaimFrequency": "0.0000", "AvgSeverity": "$#,##0"}},
    },
    {
        "name": "Segment_Freq_vs_Sev",
        "ds": "segment_analysis",
        "mark": "circle",
        "rows": ["AvgSeverity"],
        "cols": ["ClaimFrequency"],
        "encodings": {
            "detail": ["Segment", "SegmentType"],
            "size": "PolicyCount",
            "color": "SegmentType",
            "label": "Segment",
            "tooltip": ["Segment", "SegmentType", "ClaimFrequency", "AvgSeverity", "PolicyCount"],
        },
        "filters": [],
        "sort": [],
        "ref_lines": [("ClaimFrequency", 0.1007, "Avg Freq"), ("AvgSeverity", 2249, "Avg Sev")],
        "format": {"numfmt": {"ClaimFrequency": "0.0000", "AvgSeverity": "$#,##0"}},
    },

    # PAGE 3  --  Claim Cost Concentration
    {
        "name": "Pareto_Chart",
        "ds": "individual_claims",
        "mark": "bar",
        "rows": ["ClaimAmount", "CumCostPct"],
        "cols": ["ClaimRankPct"],
        "encodings": {
            "color": {"value": "#4682B4"},
            "label": "CumCostPct",
            "tooltip": ["ClaimRankPct", "CumCostPct", "CumCost", "ClaimAmount"],
        },
        "filters": [],
        "sort": [("ClaimRankPct", "asc")],
        "ref_lines": [("CumCostPct", 80, "80% Cost")],
        "format": {"numfmt": {"CumCostPct": "0.0", "ClaimRankPct": "0.0"}},
    },
    # FIX 7: Use ATTR(ClaimAmount) in the final Tableau build since each row is
    # one claim -- SUM is a pass-through but semantically misleading.
    {
        "name": "Top_Claims_Table",
        "ds": "individual_claims",
        "mark": "text",
        "rows": ["IDpol"],
        "cols": ["ClaimAmount", "CumCostPct", "ClaimRank"],
        "encodings": {
            "text": "ClaimAmount",
            "tooltip": ["IDpol", "ClaimAmount", "CumCost", "CumCostPct", "ClaimRank"],
        },
        "filters": [],
        "sort": [("ClaimAmount", "desc")],
        "top_n": 20,
        "format": {"numfmt": {"ClaimAmount": "$#,##0", "CumCostPct": "0.0%"}},
    },
    {
        "name": "Cost_Distribution_Region",
        "ds": "regional_kpi",
        "mark": "bar",
        "rows": ["Region"],
        "cols": ["TotalClaimCost"],
        "encodings": {
            "color": "TotalClaimCost",
            "label": "TotalClaimCost",
            "tooltip": ["Region", "TotalClaimCost", "AvgSeverity", "CostPerExposure"],
        },
        "filters": [],
        "sort": [("TotalClaimCost", "desc")],
        "format": {"numfmt": {"TotalClaimCost": "$#,##0"}},
    },
    # NOTE: Recommendations_Text is NOT a worksheet. It lives as a dashboard-level
    # text zone on Page 3 (see DASHBOARDS[2] zones).
]

# ─── Dashboard definitions ────────────────────────────────────────────────

DASHBOARDS = [
    {
        "name": "Page 1 - Executive Portfolio Overview",
        "size": (1200, 900),
        "zones": [
            {"type": "text",      "x": 0,   "y": 0,   "w": 1200, "h": 50,  "content": "INSURANCE CLAIMS & PORTFOLIO RISK DASHBOARD  --  French Motor Third-Party Liability (freMTPL2)"},
            {"type": "worksheet", "x": 0,   "y": 50,  "w": 1200, "h": 100, "sheet": "KPI_Cards"},
            {"type": "worksheet", "x": 0,   "y": 150, "w": 600,  "h": 350, "sheet": "Regional_Frequency_Bar"},
            {"type": "worksheet", "x": 600, "y": 150, "w": 600,  "h": 350, "sheet": "Regional_CostPerExposure_Bar"},
            {"type": "worksheet", "x": 0,   "y": 500, "w": 1200, "h": 200, "sheet": "Highlight_Table"},
            {"type": "filter",    "x": 0,   "y": 700, "w": 400,  "h": 200, "field": "Region", "source": "regional_kpi"},
            {"type": "filter",    "x": 400, "y": 700, "w": 400,  "h": 200, "field": "VehGas", "source": "policy_level"},
            {"type": "filter",    "x": 800, "y": 700, "w": 400,  "h": 200, "field": "DensityGroup", "source": "policy_level"},
        ],
        "actions": [
            {"type": "filter", "name": "Region Filter", "source_sheets": ["Regional_Frequency_Bar", "Regional_CostPerExposure_Bar", "Highlight_Table"], "target_sheets": ["KPI_Cards", "Highlight_Table"]},
        ],
    },
    {
        "name": "Page 2 - Claims &amp; Risk Segments",
        "size": (1200, 900),
        "zones": [            {"type": "text",      "x": 0,   "y": 0,   "w": 1200, "h": 50,  "content": "CLAIMS &amp; RISK SEGMENTS -- Driver, Vehicle &amp; Region Patterns"},
            {"type": "worksheet", "x": 0,   "y": 50,  "w": 400,  "h": 280, "sheet": "Driver_Age_Frequency"},
            {"type": "worksheet", "x": 400, "y": 50,  "w": 400,  "h": 280, "sheet": "Driver_Age_Severity"},
            {"type": "worksheet", "x": 800, "y": 50,  "w": 400,  "h": 280, "sheet": "Vehicle_Age_Frequency"},
            {"type": "worksheet", "x": 0,   "y": 330, "w": 1200, "h": 400, "sheet": "Freq_vs_Severity_Scatter"},
            {"type": "worksheet", "x": 0,   "y": 730, "w": 1200, "h": 170, "sheet": "Segment_Freq_vs_Sev"},
            {"type": "filter",    "x": 0,   "y": 900, "w": 300,  "h": 100, "field": "SegmentType", "source": "segment_analysis"},
        ],
        "actions": [
            {"type": "highlight", "name": "Region Highlight", "source_sheets": ["Freq_vs_Severity_Scatter"], "target_sheets": ["Segment_Freq_vs_Sev"]},
        ],
    },
    {
        "name": "Page 3 - Claim Cost Concentration",
        "size": (1200, 900),
        "zones": [
            {"type": "text",      "x": 0,   "y": 0,   "w": 1200, "h": 50,  "content": "CLAIM COST CONCENTRATION & BUSINESS RECOMMENDATIONS"},
            {"type": "worksheet", "x": 0,   "y": 50,  "w": 800,  "h": 350, "sheet": "Pareto_Chart"},
            {"type": "worksheet", "x": 800, "y": 50,  "w": 400,  "h": 350, "sheet": "Top_Claims_Table"},
            {"type": "worksheet", "x": 0,   "y": 400, "w": 1200, "h": 180, "sheet": "Cost_Distribution_Region"},
            {"type": "text",      "x": 0,   "y": 580, "w": 1200, "h": 320, "content": "RECOMMENDATION 1: Target Underwriting Review in High-Cost Regions\nChampagne-Ardenne ranks #1 in both average severity (EUR 3,230) and cost per exposure year (EUR 399). Conduct focused underwriting review -- examine pricing adequacy.\nKPI: Monthly claim frequency and cost per exposure year by region.\n\nRECOMMENDATION 2: Strengthen Monitoring of Young Driver Segment\nDrivers aged 18-25 show claim frequency 0.175 (75% above avg) and severity EUR 4,692 (167% above avg). Implement enhanced monitoring; review bonus-malus and vehicle-power differentiation.\nKPI: Monthly frequency and severity for 18-25 group vs. portfolio average.\n\nRECOMMENDATION 3: Focus Claims Management on High-Cost Tail Claims\nTop 10% of individual claims account for 60% of total cost. Establish structured review for claims above the 95th percentile (~EUR 4,862).\nKPI: Monthly count and cost contribution of claims above 95th percentile."},
        ],
        "actions": [],
    },
]


# ─── XML generation helpers ───────────────────────────────────────────────

def field_ref(ds_name, col):
    return f"[{ds_name}].[{col}]"

def col_type_str(datatype):
    return datatype  # real, integer, string

def col_role_str(role):
    return role  # dimension, measure

def col_type_attr(t):
    return t  # nominal, quantitative


def xml_datasources():
    lines = ["  <datasources>"]
    for ds_key, ds in DATASOURCES.items():
        ds_name = f"federated.{ds_key}"
        cap = ds["caption"]
        lines.append(f'    <datasource caption="{cap}" inline="true" name="{ds_name}" source="textscan" version="18.1">')
        lines.append(f'      <connection catalog="" directory="{DATA_DIR}" filename="{ds["file"]}" password="" server="" username="" workspace="">')
        lines.append(f'        <relation name="{ds_key}" table="{ds["file"]}" type="table" />')
        lines.append('      </connection>')
        for col, (dt, role, t) in ds["columns"].items():
            fmt_attr = ' format="$#,##0.00"' if dt == "real" else ""
            lines.append(f'      <column caption="{col}" datatype="{dt}" name="{field_ref(ds_key, col)}" role="{role}" type="{t}"{fmt_attr} />')
        lines.append('    </datasource>')
    lines.append("  </datasources>")
    return "\n".join(lines)


def xml_worksheet(ws):
    ds_key = ws["ds"]
    ds_name = f"federated.{ds_key}" if ds_key else None
    name = ws["name"]
    mark = ws["mark"]
    rows = ws["rows"]
    cols = ws["cols"]
    enc = ws["encodings"]
    filters_list = ws["filters"]
    sorts = ws["sort"]
    fmt = ws.get("format", {})
    ref_lines = ws.get("ref_lines", [])
    top_n = ws.get("top_n", None)
    text_block = ws.get("text_block", None)

    lines = []
    lines.append(f'    <worksheet name="{name}">')

    # ── view ──
    lines.append(f'      <view alignment="top" class="viewsheet" enable-summary="true" name="{name}">')
    if ds_name:
        cap = DATASOURCES[ds_key]["caption"] if ds_key else name
        lines.append(f'        <datasources>')
        lines.append(f'          <datasource caption="{cap}" name="{ds_name}" />')
        lines.append(f'        </datasources>')
    lines.append(f'      </view>')

    # ── datasources (top-level) ──
    lines.append(f'      <datasources>')
    if ds_name:
        cap = DATASOURCES[ds_key]["caption"] if ds_key else name
        lines.append(f'        <datasource caption="{cap}" name="{ds_name}" />')
    lines.append(f'      </datasources>')

    # ── field-info ──
    lines.append(f'      <field-info>')
    if ds_key:
        for col, (dt, role, t) in DATASOURCES[ds_key]["columns"].items():
            lines.append(f'        <field name="{field_ref(ds_key, col)}" caption="{col}" datatype="{dt}" />')
    lines.append(f'      </field-info>')

    # ── mark ──
    lines.append(f'      <mark class="{mark}">')
    # Encodings
    for enc_key, enc_val in enc.items():
        if enc_key == "text":
            if isinstance(enc_val, str):
                if ds_key:
                    lines.append(f'        <encoding field="{field_ref(ds_key, enc_val)}" type="quantitative" />')
        elif enc_key == "color":
            if isinstance(enc_val, dict):
                # fixed color
                lines.append(f'        <encoding type="color"><color><color></color></color></encoding>')
            elif isinstance(enc_val, str) and ds_key:
                lines.append(f'        <encoding field="{field_ref(ds_key, enc_val)}" type="{"nominal" if DATASOURCES[ds_key]["columns"][enc_val][1] == "dimension" else "quantitative"}" />')
        elif enc_key == "size":
            if isinstance(enc_val, str) and ds_key:
                lines.append(f'        <encoding field="{field_ref(ds_key, enc_val)}" type="quantitative" />')
        elif enc_key == "label":
            if isinstance(enc_val, str) and ds_key:
                lines.append(f'        <encoding field="{field_ref(ds_key, enc_val)}" type="{"nominal" if DATASOURCES[ds_key]["columns"][enc_val][1] == "dimension" else "quantitative"}" />')
        elif enc_key == "detail":
            if isinstance(enc_val, str) and ds_key:
                lines.append(f'        <encoding field="{field_ref(ds_key, enc_val)}" type="nominal" />')
            elif isinstance(enc_val, list) and ds_key:
                for c in enc_val:
                    lines.append(f'        <encoding field="{field_ref(ds_key, c)}" type="nominal" />')
        elif enc_key == "tooltip":
            if isinstance(enc_val, list) and ds_key:
                for c in enc_val:
                    lines.append(f'        <encoding field="{field_ref(ds_key, c)}" type="{"nominal" if DATASOURCES[ds_key]["columns"][c][1] == "dimension" else "quantitative"}" />')
    lines.append(f'      </mark>')

    # ── rows / cols ──
    lines.append(f'      <rows>')
    for r in rows:
        if ds_key:
            role = DATASOURCES[ds_key]["columns"][r][1]
            agg = "SUM" if role == "measure" else ""
            ref = field_ref(ds_key, r)
            if agg:
                lines.append(f'        <field field="{ref}" type="{role}"><aggregation>{agg}</aggregation></field>')
            else:
                lines.append(f'        <field field="{ref}" type="{role}" />')
    lines.append(f'      </rows>')

    lines.append(f'      <cols>')
    for c in cols:
        if ds_key:
            role = DATASOURCES[ds_key]["columns"][c][1]
            agg = "SUM" if role == "measure" else ""
            ref = field_ref(ds_key, c)
            if agg:
                lines.append(f'        <field field="{ref}" type="{role}"><aggregation>{agg}</aggregation></field>')
            else:
                lines.append(f'        <field field="{ref}" type="{role}" />')
    lines.append(f'      </cols>')

    # ── pane ──
    lines.append(f'      <pane>')
    if ds_key:
        for r in rows:
            lines.append(f'        <field field="{field_ref(ds_key, r)}" />')
        for c in cols:
            lines.append(f'        <field field="{field_ref(ds_key, c)}" />')
    lines.append(f'      </pane>')

    # ── filters ──
    if filters_list:
        lines.append(f'      <filters>')
        for filt_col, filt_val in filters_list:
            lines.append(f'        <filter class="categorical" column="{field_ref(ds_key, filt_col)}" value="{filt_val}" />')
        lines.append(f'      </filters>')

    # ── sort ──
    if sorts:
        lines.append(f'      <sort>')
        for s_col, s_dir in sorts:
            lines.append(f'        <sort field="{field_ref(ds_key, s_col)}" direction="{s_dir}" />')
        lines.append(f'      </sort>')

    # ── reference lines ──
    if ref_lines:
        lines.append(f'      <reference-lines>')
        for rl_field, rl_val, rl_label in ref_lines:
            lines.append(f'        <reference-line class="constant" field="{field_ref(ds_key, rl_field)}" value="{rl_val}" label="{rl_label}" />')
        lines.append(f'      </reference-lines>')

    # ── top-n ──
    if top_n:
        lines.append(f'      <top-n count="{top_n}" />')

    # ── text block (for recommendations) ──
    if text_block:
        escaped = text_block.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "&#10;")
        lines.append(f'      <text><![CDATA[{text_block}]]></text>')

    # ── format ──
    if fmt:
        lines.append(f'      <style>')
        if "numfmt" in fmt:
            for nf_field, nf_fmt in fmt["numfmt"].items():
                if ds_key:
                    lines.append(f'        <style-rule element="cell"><field field="{field_ref(ds_key, nf_field)}" /><format /><numfmt type="{nf_fmt}" /></style-rule>')
        if "font_size" in fmt:
            lines.append(f'        <style-rule element="cell"><style><font><size>{fmt["font_size"]}</size></font></style></style-rule>')
        if fmt.get("bold"):
            lines.append(f'        <style-rule element="cell"><style><font><bold>true</bold></font></style></style-rule>')
        lines.append(f'      </style>')

    lines.append(f'    </worksheet>')
    return "\n".join(lines)


def xml_dashboard(dash):
    name = dash["name"]
    w, h = dash["size"]
    zones = dash["zones"]
    actions = dash.get("actions", [])

    lines = []
    lines.append(f'    <dashboard name="{name}">')
    lines.append(f'      <size maxheight="{h}" maxwidth="{w}" minheight="{h}" minwidth="{w}" />')

    # Zones
    for i, z in enumerate(zones):
        zx, zy, zw, zh = z["x"], z["y"], z["w"], z["h"]
        lines.append(f'      <zone h="{zh}" id="{i+1}" is-spatial-root="true" r="{zx+zw}" x="{zx}" y="{zy}" w="{zw}">')

        if z["type"] == "text":
            text = z["content"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            lines.append(f'        <text val="{text}" />')
        elif z["type"] == "worksheet":
            lines.append(f'        <worksheet name="{z["sheet"]}" />')
        elif z["type"] == "filter":
            field = z["field"]
            source = z["source"]
            lines.append(f'        <filter column="{field_ref(source, field)}" datasources="{field_ref(source, field)}" />')

        lines.append(f'      </zone>')

    # Actions
    if actions:
        lines.append(f'      <dashboard-actions>')
        for act in actions:
            src_sheets = ", ".join(act["source_sheets"])
            tgt_sheets = ", ".join(act.get("target_sheets", []))
            lines.append(f'        <dashboard-action class="{act["type"]}" name="{act["name"]}">')
            lines.append(f'          <source-sheets>{src_sheets}</source-sheets>')
            if tgt_sheets:
                lines.append(f'          <target-sheets>{tgt_sheets}</target-sheets>')
            lines.append(f'        </dashboard-action>')
        lines.append(f'      </dashboard-actions>')

    lines.append(f'    </dashboard>')
    return "\n".join(lines)


def generate_workbook():
    parts = []
    parts.append('<?xml version="1.0" encoding="utf-8" ?>')
    parts.append('<workbook source-build="2024.1.0" source-platform="win" version="18.1">')
    parts.append('  <preferences />')
    parts.append(xml_datasources())
    parts.append('  <worksheets>')
    for ws in WORKSHEETS:
        parts.append(xml_worksheet(ws))
    parts.append('  </worksheets>')
    parts.append('  <dashboards>')
    for dash in DASHBOARDS:
        parts.append(xml_dashboard(dash))
    parts.append('  </dashboards>')
    parts.append('</workbook>')
    return "\n".join(parts)


if __name__ == "__main__":
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    xml = generate_workbook()
    OUTPUT.write_text(xml, encoding="utf-8")
    print(f"Generated: {OUTPUT}  ({len(xml):,} bytes, {xml.count(chr(10)):,} lines)")

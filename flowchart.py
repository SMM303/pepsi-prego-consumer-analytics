"""
How the "Pepsis" problem was discovered.
Shared data model + Plotly figure builder for the Streamlit app and the static export.

Every node carries: lane (Strategy / Process / IT & Data / Outcome), status
(verified / inference / flag), a source key, and a strategy -> process -> data chain.
"""

from __future__ import annotations

import plotly.graph_objects as go

# ---------------------------------------------------------------- sources
SOURCES = {
    "G": {
        "short": "Gladwell, TED 2004",
        "full": "Gladwell, M. (2004). Choice, happiness and spaghetti sauce. TED conference talk.",
        "url": "https://www.ted.com/talks/malcolm_gladwell_choice_happiness_and_spaghetti_sauce",
    },
    "NPR": {
        "short": "NPR TED Radio Hour 2012",
        "full": "Stewart, A. (2012). TED Radio Hour, NPR. Studio interview with Howard Moskowitz.",
        "url": "https://www.npr.org/programs/ted-radio-hour/",
    },
    "E": {
        "short": "Elberse, HBR 2008",
        "full": "Elberse, A. (2008). Should You Invest in the Long Tail? Harvard Business Review, July-Aug, reprint R0807H.",
        "url": "https://hbr.org/2008/07/should-you-invest-in-the-long-tail",
    },
    "FDA": {
        "short": "EBSCO Research Starters",
        "full": "EBSCO Research Starters. Aspartame Is Approved for Use in Carbonated Beverages (FDA final approval, 1983).",
        "url": "https://www.ebsco.com/research-starters/politics-and-government/aspartame-approved-use-carbonated-beverages",
    },
}

# ---------------------------------------------------------------- palettes
PALETTES = {
    "Midnight": dict(
        bg="#0E1422", panel="#151D30", ink="#F3EDE2", muted="#8C93A6", grid="#232C42",
        lanes={"Strategy": "#C9A45C", "Process": "#9C3D4E", "IT & Data": "#2F7A68", "Outcome": "#5C7AA8"},
        gold="#E3C17A", warn="#E07A5F", edge="#4A5370",
    ),
    "Ivory": dict(
        bg="#FBF8F2", panel="#F3EEE4", ink="#1B2233", muted="#7A7F8C", grid="#E4DDCF",
        lanes={"Strategy": "#A7843F", "Process": "#7E2C3B", "IT & Data": "#245E51", "Outcome": "#3E5A86"},
        gold="#A7843F", warn="#B5482E", edge="#B9B2A3",
    ),
}

LANES = ["Strategy", "Process", "IT & Data", "Outcome"]
LANE_Y = {"Strategy": 4, "Process": 3, "IT & Data": 2, "Outcome": 1}

# ---------------------------------------------------------------- nodes
# group: core | default | moskowitz | validation | course
NODES = [
    dict(id="N1", step=1, x=1, y=4.0, lane="Strategy", group="core",
         title="Strategic goal", text="Diet Pepsi<br>with aspartame",
         status="flag", src="G",
         note="Pepsi brief to Moskowitz. Gladwell dates it 'early 70s'. Aspartame only got US approval for soft drinks in 1983, so the date is unverified.",
         chain="Strategy: enter diet cola with a new sweetener -> Process: product formulation brief -> Data: none yet, target is one dose per can"),
    dict(id="N2", step=2, x=2, y=3.0, lane="Process", group="core",
         title="Problem framed", text="Find THE sweet spot<br>in an 8–12% band",
         status="verified", src="G",
         note="Pepsi: below 8% not sweet enough, above 12% too sweet. Question asked: what single level is perfect?",
         chain="Strategy: one product for everyone -> Process: single-optimum search -> Data: one target variable (sweetness %)"),
    dict(id="N3", step=3, x=3, y=2.0, lane="IT & Data", group="core",
         title="Test design", text="0.1% steps, 8–12%<br>thousands tasted",
         status="verified", src="G",
         note="8.0, 8.1 ... 12.0. Tested on thousands of people, results plotted on one curve, take the most popular level.",
         chain="Strategy: one SKU -> Process: aggregate taste test -> Data: pooled ratings, one curve, look for the peak"),
    dict(id="N4", step=4, x=4, y=1.0, lane="Outcome", group="core",
         title="Result", text="No bell curve.<br>Data 'a mess'",
         status="verified", src="G",
         note="The pooled curve had no clean peak. Gladwell: 'it's all over the place'.",
         chain="Data signal: high variance, no single mode -> the model (one population) does not fit the market"),
    # default branch
    dict(id="N5", step=5, x=5, y=3.0, lane="Process", group="default",
         title="Industry habit", text="Assume error,<br>pick 10% midpoint",
         status="verified", src="G",
         note="Most food testers treat messy data as noise and make an 'educated guess' in the middle.",
         chain="Process keeps the old frame -> analysis = compromise -> the data's warning is ignored"),
    dict(id="N6", step=6, x=6, y=1.0, lane="Outcome", group="default",
         title="Middling product", text="Subgroups<br>averaged away",
         status="inference", src=None,
         note="INFERENCE. Not stated in the sources. A midpoint pleases no cluster fully; Gladwell's coffee figures (about 60/100 for one blend) show the cost.",
         chain="Averaging heterogeneous demand -> mediocre fit -> lower scores, no segment owned"),
    # Moskowitz branch
    dict(id="N7", step=5, x=5, y=2.0, lane="IT & Data", group="moskowitz",
         title="Re-reads the test", text="'Bedevilled him<br>for years'",
         status="verified", src="G",
         note="Moskowitz will not accept the 10% guess. He keeps asking why the experiment fails.",
         chain="Analyst challenges the process, not the data"),
    dict(id="N8", step=6, x=7, y=4.0, lane="Strategy", group="moskowitz",
         title="Reframe", text="Perfect Pepsi ✗<br>Perfect PepsiS ✓",
         status="verified", src="G",
         note="The insight in a White Plains diner: Pepsi asked the wrong question. Plural optimum, one per taste group.",
         chain="Strategy: portfolio of products -> Process: segment-first testing -> Data: cluster analysis, not one peak"),
    dict(id="N9", step=7, x=8, y=3.0, lane="Process", group="moskowitz",
         title="Market rejects idea", text="Conferences, no<br>clients for years",
         status="verified", src="G",
         note="Industry not ready. No one hires him on this idea for years.",
         chain="Org readiness gap: the capability exists, the strategy does not"),
    # validation
    dict(id="N10", step=8, x=9, y=2.0, lane="IT & Data", group="validation",
         title="Proof 1: Vlasic", text="Perfect pickleS<br>→ Zesty line",
         status="verified", src="G",
         note="Recommendation: improve regular AND create zesty.",
         chain="Segment found -> new SKU (Zesty)"),
    dict(id="N11", step=9, x=10, y=2.0, lane="IT & Data", group="validation",
         title="Proof 2: Prego", text="45 sauces, 4 cities<br>0–100 ratings",
         status="verified", src="G",
         note="Campbell's kitchen built 45 variants (sweetness, garlic, tartness, visible solids). NY, Chicago, Jacksonville, LA. Data grouped into clusters, not ranked.",
         chain="Strategy: fix a struggling brand -> Process: designed variation + central-location tests -> Data: ratings matrix -> clustering"),
    dict(id="N12", step=10, x=11, y=1.0, lane="Outcome", group="validation",
         title="Payoff", text="Plain·Spicy·Chunky<br>~$600M / 10 yrs",
         status="flag", src="G",
         note="About one third preferred extra chunky; no one sold it. $600M is Gladwell's figure, not audited company data.",
         chain="Unserved cluster -> new line -> revenue"),
    dict(id="N13", step=11, x=12, y=4.0, lane="Strategy", group="validation",
         title="Doctrine", text="Horizontal<br>segmentation",
         status="verified", src="G",
         note="Taste is not a hierarchy (Grey Poupon model). Different products for different people. Ragu later: 36 SKUs in 6 varieties.",
         chain="Strategy now drives assortment breadth -> process + data must support many SKUs"),
    dict(id="N14", step=11, x=12, y=1.0, lane="Outcome", group="validation",
         title="Coffee test", text="1 blend ≈ 60/100<br>clusters → 75–78",
         status="verified", src="G",
         note="Moskowitz's Nescafé work as told by Gladwell.",
         chain="Clustered offer lifts liking about 15–18 points"),
    # course link
    dict(id="L1", step=11, x=12, y=2.0, lane="IT & Data", group="course",
         title="Long-tail check", text="Top 10% of tracks<br>= 78% of plays",
         status="verified", src="E",
         note="Elberse (2008): the tail gets longer but flatter; hits still dominate. Segment where clusters are big enough to pay.",
         chain="Segmentation has a floor: cluster size x margin must cover SKU cost"),
]

# ---------------------------------------------------------------- edges
# (from, to, groups it belongs to)
EDGES = [
    ("N1", "N2", {"core"}),
    ("N2", "N3", {"core"}),
    ("N3", "N4", {"core"}),
    ("N4", "N5", {"default"}),
    ("N5", "N6", {"default"}),
    ("N4", "N7", {"moskowitz"}),
    ("N7", "N8", {"moskowitz"}),
    ("N8", "N9", {"moskowitz"}),
    ("N9", "N10", {"validation"}),
    ("N10", "N11", {"validation"}),
    ("N11", "N12", {"validation"}),
    ("N12", "N13", {"validation"}),
    ("N12", "N14", {"validation"}),
    ("N11", "L1", {"course"}),
]

PATHS = {
    "Full map": None,
    "Industry default": {"N1", "N2", "N3", "N4", "N5", "N6"},
    "Moskowitz path": {"N1", "N2", "N3", "N4", "N7", "N8", "N9", "N10", "N11", "N12", "N13"},
}

# misalignment markers: placed on edges where strategy and data design diverge
MISALIGN = [
    dict(between=("N2", "N3"), at=(0.45, 2.0),
         text="⚠ Misalignment: strategy assumed one market,<br>so data design looked for one peak"),
    dict(between=("N4", "N5"), at=(4.62, 3.64),
         text="⚠ Signal ignored: variance read as error"),
]

BOX_W, BOX_H = 0.8, 0.62
GAP = 1 - BOX_W
XMAX = 12.6


def _node(nid):
    return next(n for n in NODES if n["id"] == nid)


def _rounded(x0, y0, x1, y1, r=0.07):
    ry = r * 0.9
    return (f"M {x0 + r},{y0} L {x1 - r},{y0} Q {x1},{y0} {x1},{y0 + ry} "
            f"L {x1},{y1 - ry} Q {x1},{y1} {x1 - r},{y1} L {x0 + r},{y1} "
            f"Q {x0},{y1} {x0},{y1 - ry} L {x0},{y0 + ry} Q {x0},{y0} {x0 + r},{y0} Z")


def visible_nodes(lanes, overlays, max_step):
    out = []
    for n in NODES:
        if n["lane"] not in lanes or n["step"] > max_step:
            continue
        if n["group"] == "validation" and "Validation cases" not in overlays:
            continue
        if n["group"] == "course" and "Long-tail link" not in overlays:
            continue
        if n["status"] == "inference" and "Inferences" not in overlays:
            continue
        out.append(n)
    return out


def build_figure(theme="Midnight", lanes=tuple(LANES),
                 overlays=("Validation cases", "Inferences", "Misalignment flags", "Source tags", "Long-tail link"),
                 path="Full map", max_step=11, selected=None, width=1920, height=1080, title=True):
    P = PALETTES[theme]
    nodes = visible_nodes(lanes, overlays, max_step)
    ids = {n["id"] for n in nodes}
    hl = PATHS[path]

    fig = go.Figure()
    shapes, ann = [], []

    # lane bands
    for lane in LANES:
        y = LANE_Y[lane]
        on = lane in lanes
        shapes.append(dict(type="rect", xref="x", yref="y", x0=0.35, x1=XMAX, y0=y - 0.5, y1=y + 0.5,
                           fillcolor=P["panel"] if y % 2 == 0 else P["bg"], line=dict(width=0), layer="below"))
        shapes.append(dict(type="line", x0=0.35, x1=XMAX, y0=y - 0.5, y1=y - 0.5,
                           line=dict(color=P["grid"], width=1), layer="below"))
        ann.append(dict(x=0.05, y=y, xref="x", yref="y", text=f"<b>{lane.upper()}</b>",
                        showarrow=False, textangle=-90, xanchor="center",
                        font=dict(size=12, color=P["lanes"][lane] if on else P["muted"],
                                  family="Aptos, Segoe UI, Helvetica")))

    # edges as arrows
    for a, b, groups in EDGES:
        if a not in ids or b not in ids:
            continue
        na, nb = _node(a), _node(b)
        on_path = hl is None or (a in hl and b in hl)
        # elbow connector: out of A's right edge, vertical in the gap left of B, into B's left edge
        sx, sy = na["x"] + BOX_W / 2, na["y"]
        ex, ey = nb["x"] - BOX_W / 2, nb["y"]
        xv = ex - GAP / 2
        color = P["gold"] if (hl is not None and on_path) else (P["edge"] if on_path else P["grid"])
        aw = 3.0 if (hl is not None and on_path) else 1.6
        shapes.append(dict(type="path", xref="x", yref="y",
                           path=f"M {sx},{sy} L {xv},{sy} L {xv},{ey} L {ex - 0.02},{ey}",
                           line=dict(color=color, width=aw), opacity=1 if on_path else 0.4, layer="below"))
        ann.append(dict(x=ex, y=ey, ax=ex - 0.06, ay=ey, xref="x", yref="y", axref="x", ayref="y",
                        showarrow=True, arrowhead=2, arrowsize=1.0, arrowwidth=aw,
                        arrowcolor=color, opacity=1 if on_path else 0.4, text=""))

    # misalignment flags
    if "Misalignment flags" in overlays:
        for m in MISALIGN:
            a, b = m["between"]
            if a in ids and b in ids:
                mx, my = m["at"]
                ann.append(dict(x=mx, y=my, xref="x", yref="y", text=m["text"],
                                showarrow=False, xanchor="left", align="left",
                                font=dict(size=10.5, color=P["warn"], family="Aptos, Segoe UI, Helvetica"),
                                bgcolor=P["bg"], bordercolor=P["warn"], borderwidth=1, borderpad=4))

    # nodes
    for n in nodes:
        c = P["lanes"][n["lane"]]
        on_path = hl is None or n["id"] in hl
        is_sel = selected == n["id"]
        dash = "dot" if n["status"] == "inference" else "solid"
        x0, x1 = n["x"] - BOX_W / 2, n["x"] + BOX_W / 2
        y0, y1 = n["y"] - BOX_H / 2, n["y"] + BOX_H / 2
        shapes.append(dict(type="path", path=_rounded(x0, y0, x1, y1), xref="x", yref="y",
                           fillcolor=c if on_path else P["panel"],
                           opacity=1 if on_path else 0.45,
                           line=dict(color=P["gold"] if (is_sel or (hl and on_path)) else c,
                                     width=3 if is_sel else (2 if hl and on_path else 1.2), dash=dash)))
        txt_col = "#FFFFFF" if on_path else P["muted"]
        ann.append(dict(x=n["x"], y=n["y"] + 0.13, xref="x", yref="y",
                        text=f"<b>{n['title']}</b>", showarrow=False,
                        font=dict(size=11, color=txt_col, family="Aptos, Segoe UI, Helvetica")))
        ann.append(dict(x=n["x"], y=n["y"] - 0.07, xref="x", yref="y", text=n["text"],
                        showarrow=False, font=dict(size=11, color=txt_col, family="Aptos, Segoe UI, Helvetica")))
        # status / source badge
        badge = {"verified": "✓", "inference": "INF", "flag": "!"}[n["status"]]
        if "Source tags" in overlays:
            src = SOURCES[n["src"]]["short"] if n["src"] else "no source"
            ann.append(dict(x=n["x"], y=y0 - 0.06, xref="x", yref="y",
                            text=f"{badge} {src}", showarrow=False,
                            font=dict(size=8.5, color=P["warn"] if n["status"] != "verified" else P["muted"],
                                      family="Aptos, Segoe UI, Helvetica")))

    # click targets
    fig.add_trace(go.Scatter(
        x=[n["x"] for n in nodes], y=[n["y"] for n in nodes], mode="markers",
        marker=dict(size=46, symbol="square", color="rgba(0,0,0,0.01)"),
        customdata=[[n["id"], n["title"], n["note"], n["chain"],
                     SOURCES[n["src"]]["short"] if n["src"] else "INFERENCE, no source"] for n in nodes],
        hovertemplate="<b>%{customdata[1]}</b><br>%{customdata[2]}<br><br>"
                      "<i>%{customdata[3]}</i><br>Source: %{customdata[4]}<extra></extra>",
        hoverlabel=dict(bgcolor=P["panel"], font=dict(color=P["ink"], size=11), bordercolor=P["gold"]),
        showlegend=False, name="nodes",
    ))

    if title:
        ann.append(dict(x=0.35, y=4.78, xref="x", yref="y", xanchor="left", showarrow=False,
                        text="<b>From the perfect Pepsi to the perfect Pepsis</b>"
                             f"<span style='font-size:12px;color:{P['muted']}'>   "
                             "how a messy curve exposed a strategy-data misalignment</span>",
                        font=dict(size=20, color=P["ink"], family="Georgia, Cormorant Garamond, serif")))
        ann.append(dict(x=XMAX, y=0.32, xref="x", yref="y", xanchor="right", showarrow=False,
                        text="✓ verified   ! date/figure unverified   INF inference (dotted)   "
                             "Sources: Gladwell TED 2004; NPR 2012; Elberse HBR 2008; EBSCO/FDA 1983",
                        font=dict(size=9, color=P["muted"], family="Aptos, Segoe UI, Helvetica")))

    fig.update_layout(
        shapes=shapes, annotations=ann, width=width, height=height,
        paper_bgcolor=P["bg"], plot_bgcolor=P["bg"], margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(range=[-0.15, XMAX + 0.1], visible=False, fixedrange=False),
        yaxis=dict(range=[0.2, 5.0], visible=False, fixedrange=True),
        dragmode="pan", clickmode="event+select", hovermode="closest",
        font=dict(family="Aptos, Segoe UI, Helvetica"),
    )
    return fig

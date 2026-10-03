"""
MSBA310 | Q3 | How the "Pepsis" problem was discovered
Interactive flow chart: Strategy -> Process -> IT & Data -> Outcome.

Run:   streamlit run app.py
"""
import os

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from flowchart import LANES, NODES, PATHS, PALETTES, SOURCES, XMAX, build_figure

st.set_page_config(page_title="Perfect Pepsis | Flow", page_icon="◆", layout="wide")

# ---------------------------------------------------------------- state
ss = st.session_state
ss.setdefault("step", 11)
ss.setdefault("selected", None)

# ---------------------------------------------------------------- sidebar controls
with st.sidebar:
    st.markdown("### Controls")
    theme = st.segmented_control("Theme", list(PALETTES), default="Midnight", key="theme") or "Midnight"
    path = st.segmented_control("Highlight path", list(PATHS), default="Moskowitz path", key="path") or "Full map"
    lanes = st.pills("Lanes", LANES, selection_mode="multi", default=LANES, key="lanes")
    overlays = st.pills(
        "Layers",
        ["Validation cases", "Inferences", "Misalignment flags", "Source tags", "Long-tail link"],
        selection_mode="multi",
        default=["Validation cases", "Inferences", "Misalignment flags", "Source tags"],
        key="overlays",
    )
    st.divider()
    st.caption("✓ verified in source  ·  ! date or figure not verified  ·  INF inference (dotted box)")

P = PALETTES[theme]
st.markdown(
    f"""
    <style>
      .stApp {{ background:{P['bg']}; color:{P['ink']}; }}
      h1, h2, h3 {{ font-family: Georgia, 'Cormorant Garamond', serif; color:{P['ink']}; letter-spacing:.2px; }}
      .card {{ background:{P['panel']}; border-left:4px solid {P['gold']}; padding:14px 18px;
               border-radius:6px; font-family:Aptos, 'Segoe UI', sans-serif; font-size:14px; }}
      .chain {{ color:{P['gold']}; font-style:italic; }}
      .muted {{ color:{P['muted']}; font-size:12.5px; }}
      section[data-testid="stSidebar"] {{ background:{P['panel']}; }}
      section[data-testid="stSidebar"] * {{ color:{P['ink']}; }}
      section[data-testid="stSidebar"] button {{ background:{P['bg']}; }}
      header[data-testid="stHeader"] {{ background:{P['bg']}; }}
      .stButton button {{ background:{P['panel']}; color:{P['ink']}; border:1px solid {P['gold']}; }}
      .stButton button:hover {{ border-color:{P['ink']}; color:{P['gold']}; }}
      [data-testid="stWidgetLabel"] p, .stCaption, label {{ color:{P['muted']} !important; }}

    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("## From the perfect Pepsi to the perfect Pepsis")
st.caption("Click a box for its strategy → process → data chain. Step through the story with the slider or the buttons.")

# ---------------------------------------------------------------- step-through
c1, c2, c3, c4 = st.columns([1, 1, 1, 7], vertical_alignment="bottom")
if c1.button("⏮ Start", use_container_width=True):
    ss.step = 1
if c2.button("◀ Back", use_container_width=True):
    ss.step = max(1, ss.step - 1)
if c3.button("Next ▶", use_container_width=True):
    ss.step = min(11, ss.step + 1)
c4.slider("Reveal up to step", 1, 11, key="step")

# ---------------------------------------------------------------- chart
fig = build_figure(theme=theme, lanes=tuple(lanes or []), overlays=tuple(overlays or []),
                   path=path, max_step=ss.step, selected=ss.selected, width=None, height=780, title=False)
fig.update_layout(autosize=True, width=None, margin=dict(l=90, r=10, t=10, b=10))
# lane names as fixed y-axis labels so they stay put while panning
fig.update_yaxes(visible=True, tickvals=[4, 3, 2, 1], ticktext=[f"<b>{l}</b>" for l in LANES],
                 showgrid=False, zeroline=False, showline=False, ticks="",
                 tickfont=dict(size=12, color=P["gold"], family="Aptos, Segoe UI"))

# camera: a 7-column window that follows the current step; drag to pan along the lines
whole = st.toggle("Show whole map", value=False, help="Off: the view follows the step slider. Drag sideways to scroll.")
if not whole:
    span = 6.9
    lo = min(max(-0.15, ss.step - 5.4), XMAX + 0.1 - span)
    fig.update_xaxes(range=[lo, lo + span])
st.caption("Drag sideways to scroll the lines. Scroll wheel zooms. Double-click resets.")
event = st.plotly_chart(
    fig, use_container_width=True, on_select="rerun", selection_mode="points", key="flow",
    config={"displaylogo": False, "scrollZoom": True, 
            "toImageButtonOptions": {"format": "png", "filename": "pepsis_flow", "width": 1920, "height": 1080, "scale": 2}},
)
pts = (event or {}).get("selection", {}).get("points", []) if event else []
if pts:
    ss.selected = pts[0]["customdata"][0]

# ---------------------------------------------------------------- detail card
node = next((n for n in NODES if n["id"] == ss.selected), None)
left, right = st.columns([3, 2])
with left:
    if node:
        src = SOURCES.get(node["src"])
        src_html = f"<a href='{src['url']}' target='_blank'>{src['full']}</a>" if src else "<b>INFERENCE</b>. No source states this."
        st.markdown(
            f"""<div class='card'><b>{node['title']}</b> · <span class='muted'>{node['lane']} lane · {node['status']}</span><br>
            {node['note']}<br><br><span class='chain'>{node['chain'].replace('->', '→')}</span><br><br>
            <span class='muted'>{src_html}</span></div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown("<div class='card'>Select a box to see its chain and source.</div>", unsafe_allow_html=True)

with right:
    # Gladwell's coffee figures: the measurable cost of the single-product frame
    bar = go.Figure(go.Bar(
        x=["One blend", "Clusters, low", "Clusters, high"],
        y=[60, 75, 78], marker_color=[P["muted"], P["lanes"]["IT & Data"], P["gold"]],
        text=[60, 75, 78], textposition="outside",
    ))
    bar.update_layout(height=260, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor=P["bg"], plot_bgcolor=P["bg"],
                      font=dict(color=P["ink"], family="Aptos, Segoe UI"), yaxis=dict(range=[0, 100], title="Mean liking, 0–100"),
                      title=dict(text="Coffee liking: one product vs clusters (Gladwell 2004)", font=dict(size=13)))
    st.plotly_chart(bar, use_container_width=True, config={"displaylogo": False})

# ---------------------------------------------------------------- evidence table
with st.expander("Evidence table (every node, status, source)"):
    df = pd.DataFrame([{
        "Step": n["step"], "Node": n["title"], "Lane": n["lane"], "Status": n["status"],
        "Chain": n["chain"].replace("->", "→"),
        "Source": SOURCES[n["src"]]["url"] if n["src"] else None,
    } for n in NODES]).sort_values("Step")
    st.dataframe(df, hide_index=True, use_container_width=True, column_config={
        "Source": st.column_config.LinkColumn("Source", display_text=r"https?://(?:www\.)?([^/]+)"),
        "Chain": st.column_config.TextColumn(width="large"),
    })

# ---------------------------------------------------------------- export
with st.expander("Export slide image"):
    st.caption("1920×1080 PNG at 2x. Uses Kaleido, which needs Chrome. If it fails: python -c \"import kaleido; kaleido.get_chrome_sync()\"")
    exp_theme = st.radio("Slide theme", list(PALETTES), index=1, horizontal=True)
    if st.button("Render PNG"):
        try:
            img = build_figure(theme=exp_theme, lanes=tuple(lanes or []), overlays=tuple(overlays or []),
                               path=path, max_step=11).to_image(format="png", width=1920, height=1080, scale=2)
            st.download_button("Download PNG", img, file_name="pepsis_flow.png", mime="image/png")
        except Exception as e:  # noqa: BLE001
            st.error(f"Export failed: {e}")

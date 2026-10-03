"""Export slide-ready static images of the flow chart (16:9).

    python export_png.py            -> pepsis_flow_ivory.png, pepsis_flow_midnight.png
"""
import os
import sys

from flowchart import build_figure

# Kaleido 1.x drives a local Chrome/Chromium. If none is found, run once:
#     python -c "import kaleido; kaleido.get_chrome_sync()"
if os.path.exists("/opt/pw-browsers/chromium-1194/chrome-linux/chrome"):
    os.environ.setdefault("BROWSER_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")

out = sys.argv[1] if len(sys.argv) > 1 else "."
for theme in ("Ivory", "Midnight"):
    fig = build_figure(theme=theme, path="Moskowitz path")
    path = os.path.join(out, f"pepsis_flow_{theme.lower()}.png")
    fig.write_image(path, width=1920, height=1080, scale=2)
    print("wrote", path)

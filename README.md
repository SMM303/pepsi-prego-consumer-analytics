# Q3 flow chart: from the perfect Pepsi to the perfect Pepsis

## Run (Windows / macOS)
    python -m venv .venv
    .venv\Scripts\activate          (macOS: source .venv/bin/activate)
    pip install -r requirements.txt
    streamlit run app.py

Opens at http://localhost:8501.

## Controls
- Sidebar: theme, highlight path (gold arrows), lanes on/off, layers on/off
  (validation cases, inferences, misalignment flags, source tags, long-tail link).
- Start / Back / Next or the slider: reveal the story step by step. The view follows the step.
- "Show whole map" toggle: see everything at once. Drag sideways to scroll, wheel to zoom.
- Click a box: card shows its strategy -> process -> data chain and the source link.
- Evidence table: every node, status (verified / flag / inference), source URL.

## Slide image
    python export_png.py
writes pepsis_flow_ivory.png and pepsis_flow_midnight.png (1920x1080 @2x).
Kaleido needs Chrome. If export fails, run once:
    python -c "import kaleido; kaleido.get_chrome_sync()"

## Files
- flowchart.py  nodes, sources, edges, figure builder (edit content here)
- app.py        Streamlit UI
- export_png.py static export

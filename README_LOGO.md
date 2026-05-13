# Logo Background Removal And Animation

This document explains how to create a transparent version of the AyurAI logo and preview a simple animation.

Files added:
- `scripts/remove_bg.py` - Python script using `rembg` and `Pillow` to remove the background and save a transparent PNG.
- `frontend/logo_demo.html` - Standalone demo page that shows how to animate the transparent PNG with CSS and JavaScript.

Quick steps:

1. Save the source logo image as `assets/logo_source.png`.
2. Install dependencies in your virtual environment:

```powershell
pip install rembg pillow
```

3. Run the removal script:

```powershell
python scripts\remove_bg.py assets\logo_source.png assets\logo_transparent.png
```

4. Open `frontend/logo_demo.html` with a local static server to preview the animation.

Exporting animated assets:
- To export GIF, WebP, or MP4, record the browser preview and convert it with `ffmpeg`.

Example:

```powershell
ffmpeg -i input.mp4 -vf "fps=15,scale=800:-1:flags=lanczos" -loop 0 output.gif
```

Notes:
- The demo expects the transparent file at `assets/logo_transparent.png`.
- These files are optional helpers and do not affect the main app unless you choose to run or integrate them.

"""Build the single V2 entry point with bundled fonts and no CDN/build dependency."""

import base64
import re
from pathlib import Path

ROOT = Path(__file__).parent / "preview"
html = (ROOT / "studio.template.html").read_text()
html = re.sub(
    r'<link\s+rel="stylesheet"\s+href="/studio.css"\s*/?>',
    lambda _: "<style>\n" + (ROOT / "studio.css").read_text() + "\n</style>",
    html,
)
for name in [
    "cv-upload.js",
    "visual-design.js",
    "islands.js",
    "journey.js",
    "dna.js",
    "studio.js",
]:
    pattern = r'<script\s+src="/' + re.escape(name) + r'"\s*>\s*</script>'
    html, count = re.subn(
        pattern,
        lambda _: "<script>\n" + (ROOT / name).read_text() + "\n</script>",
        html,
    )
    if count != 1:
        raise ValueError("Expected one script entry for " + name)
for name in ["pm-heading.ttf", "pm-body.ttf"]:
    html = html.replace(
        "/assets/" + name,
        "data:font/ttf;base64,"
        + base64.b64encode((ROOT / "assets" / name).read_bytes()).decode(),
    )
(ROOT / "index.html").write_text(html)
print("Built Career DNA V2 preview/index.html")

"""Bundle the preview with no install, network request or external build tool."""
from pathlib import Path
import base64
root=Path(__file__).parent/'preview'
html=(root/'studio.template.html').read_text()
html=html.replace('<link rel="stylesheet" href="/studio.css">','<style>\n'+(root/'studio.css').read_text()+'\n</style>')
html=html.replace('<script src="/pm-library.js"></script>','<script>\n'+(root/'pm-library.js').read_text()+'\n</script>')
html=html.replace('<script src="/pm-fonts.js"></script>','<script>\n'+(root/'pm-fonts.js').read_text()+'\n</script>')
html=html.replace('<script src="/poster.js"></script>','<script>\n'+(root/'poster.js').read_text()+'\n</script>')
html=html.replace('<script src="/studio.js"></script>','<script>\n'+(root/'studio.js').read_text()+'\n</script>')
for asset in ['pm-career-dna-logo.png','career-world-atlas.png','pm-characters-24.png','pm-icons-24.png']:
 html=html.replace('/assets/'+asset,'data:image/png;base64,'+base64.b64encode((root/'assets'/asset).read_bytes()).decode())
for asset in ['pm-heading.ttf','pm-body.ttf']:
 html=html.replace('/assets/'+asset,'data:font/ttf;base64,'+base64.b64encode((root/'assets'/asset).read_bytes()).decode())
(root/'index.html').write_text(html)
print('Bundled preview/index.html')

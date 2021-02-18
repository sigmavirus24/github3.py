import tempfile
import webbrowser

import github4

template = """<html><head></head><body>{0}</body></html>"""

i = github4.issue("kennethreitz", "requests", 868)

with tempfile.NamedTemporaryFile() as tmpfd:
    tmpfd.write(template.format(i.body_html))
    webbrowser.open("file://" + tmpfd.name)

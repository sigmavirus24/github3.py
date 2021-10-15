#!/usr/bin/env python
import glob

from IPython.config import Config
from IPython.nbconvert import HTMLExporter

c = Config({"ExecutePreprocessor": {"enabled": True}})

exporter = HTMLExporter(config=c)

for filename in glob.glob("example-notebooks/*.ipynb"):
    print(filename)
    exporter.from_filename(filename)

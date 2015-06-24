#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import json

from IPython.config import Config
from IPython.nbconvert import ExecutePreprocessor
from IPython.nbconvert import HTMLExporter
from IPython.nbformat import NotebookNode

c = Config({
    'ExecutePreprocessor': {'enabled': True}
})

exporter = HTMLExporter(config=c)
executor = ExecutePreprocessor(config=c)

for filename in glob.glob("example-notebooks/*.ipynb"):
    print(filename)
    exporter.from_filename(filename)
    with open(filename, 'r') as file:
        node = NotebookNode(json.load(file))
    executor.preprocess(node, {})

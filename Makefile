# Makefile for github3.py
#
# Copyright 2012, Ian Cordasco

COVERAGE_INCLUDE := github3/*.py

clean:
	git clean -Xdf

travis:
	python mocktests.py

tests: travis

docs:
	make -C docs/ html

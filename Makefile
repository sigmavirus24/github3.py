# Makefile for github3.py
#
# Copyright 2015, Ian Cordasco

COVERAGE_INCLUDE := github3/*.py
TEST_RUNNER := tox

.DEFAULT_GOAL := tests

clean:
	git clean -Xdf
	rm -rf build/ dist/

ga:
	$(TEST_RUNNER)

tests: ga

test-deps:
	pip install -e .[dev]

htmlcov: .coverage
	coverage html --omit=github3/packages/*

docs: docs/*.rst
	tox -e docs

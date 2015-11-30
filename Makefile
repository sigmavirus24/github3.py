# Makefile for github3.py
#
# Copyright 2015, Ian Cordasco

COVERAGE_INCLUDE := github3/*.py
TEST_RUNNER := tox

.DEFAULT_GOAL := tests

clean:
	git clean -Xdf
	rm -rf build/ dist/

travis:
	$(TEST_RUNNER)

tests: travis

test-deps:
	pip install -r dev-requirements.txt

htmlcov: .coverage
	coverage html --omit=github3/packages/*

docs: docs/*.rst
	tox -e docs

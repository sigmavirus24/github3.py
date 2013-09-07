# Makefile for github3.py
#
# Copyright 2012, Ian Cordasco

COVERAGE_INCLUDE := github3/*.py
TEST_RUNNER := python setup.py test

.DEFAULT_GOAL := tests

clean:
	git clean -Xdf
	rm -rf build/ dist/

travis:
	$(TEST_RUNNER)

tests: travis

test-deps:
	pip install -r requirements.txt

htmlcov: .coverage
	coverage html --omit=github3/packages/*

docs:
	make -C docs/ html

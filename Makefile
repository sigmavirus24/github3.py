# Makefile for github3.py
#
# Copyright 2012, Ian Cordasco

COVERAGE_INCLUDE := github3/*.py
TEST_RUNNER := run_tests.py

clean:
	git clean -Xdf
	rm -rf build/ dist/

travis:
	python $(TEST_RUNNER)

tests: travis

htmlcov: .coverage
	coverage html --omit=github3/packages/*

docs:
	make -C docs/ html

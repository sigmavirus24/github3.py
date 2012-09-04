# Makefile for github3.py
#
# Copyright 2012, Ian Cordasco

COVERAGE_INCLUDE := github3/*.py

clean:
	git clean -Xdf

travis:
	CI=true ./unittests.py

tests: travis

alltests:
	./unittests.py

docs:
	make -C docs/ html

coverage_all:
	coverage run --include=$(COVERAGE_INCLUDE) ./unittests.py
	coverage report

coverage_auth: coverage_all

coverage:
	CI=true coverage run --include=$(COVERAGE_INCLUDE) ./unittests.py
	coverage report

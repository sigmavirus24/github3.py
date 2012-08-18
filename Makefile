# Makefile for github3.py
#
# Copyright 2012, Ian Cordasco

clean:
	git clean -Xdf

travis:
	CI=true ./unittests.py

tests: travis

alltests:
	./unittests.py

docs:
	make -C docs/ html

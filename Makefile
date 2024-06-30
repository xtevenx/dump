.DEFAULT_GOAL := all

symmetric_nonbipartite: symmetric_nonbipartite.py template.html
	python symmetric_nonbipartite.py

all: symmetric_nonbipartite

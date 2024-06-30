.DEFAULT_GOAL := all

symmetric_nonbipartite: symmetric_nonbipartite.py symmetric_nonbipartite.template
	python symmetric_nonbipartite.py

all: symmetric_nonbipartite

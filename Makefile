all: symmetric_nonbipartite.html two_distinct_eigenvalues.html

symmetric_nonbipartite.html: symmetric_nonbipartite.py template.html
	python symmetric_nonbipartite.py

two_distinct_eigenvalues.html: two_distinct_eigenvalues.py template.html
	python two_distinct_eigenvalues.py

all: symmetric_nonbipartite.html
all: two_distinct_eigenvalues.html

symmetric_nonbipartite.html: symmetric_nonbipartite.py template.html
	python symmetric_nonbipartite.py

two_distinct_eigenvalues.html: two_distinct_eigenvalues.py template.html
	python two_distinct_eigenvalues.py

clean:
	rm -r symmetric_nonbipartite/ || true
	rm -r two_distinct_eigenvalues/ || true
	touch template.html

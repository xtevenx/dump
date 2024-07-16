all: integer_eigenvalues.html
all: small_tournaments.html
all: small_tournaments_mixed.html
all: symmetric_nonbipartite.html
all: two_distinct_eigenvalues.html

integer_eigenvalues.html: integer_eigenvalues.py template.html
	python integer_eigenvalues.py

small_tournaments.html: small_tournaments.py template.html
	python small_tournaments.py

small_tournaments_mixed.html: small_tournaments_mixed.py template.html
	python small_tournaments_mixed.py

symmetric_nonbipartite.html: symmetric_nonbipartite.py template.html
	python symmetric_nonbipartite.py

two_distinct_eigenvalues.html: two_distinct_eigenvalues.py template.html
	python two_distinct_eigenvalues.py

clean:
	rm -r __pycache__ || true
	rm -r integer_eigenvalues/ || true
	rm -r small_tournaments/ || true
	rm -r small_tournaments_mixed/ || true
	rm -r symmetric_nonbipartite/ || true
	rm -r two_distinct_eigenvalues/ || true
	touch template.html

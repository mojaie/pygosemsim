
builddocs:
	cd docs; make html

test:
	@python3 -m unittest discover -s pygosemsim/test

pf:
	@python3 -m unittest pygosemsim.test.performance.TestPerformance

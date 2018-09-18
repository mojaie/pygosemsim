
builddocs:
	cd docs; make html

test:
	@python3 -m unittest discover -s pygosemsim/test

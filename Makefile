pypi:
	mkdir -p dist
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/* -u omegaml
	@echo now test your package!

pypi-prod:
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/* -u omegaml


	

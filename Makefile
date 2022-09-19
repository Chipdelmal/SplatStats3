SHELL=bash
python=python
pip=pip
tests=.
version:=$(shell $(python) version.py)
sdist_name:=SplatStats-$(version).tar.gz

develop:
	$(pip) install -e .

clean_develop:
	- $(pip) uninstall -y MK8D
	- rm -rf *.egg-info

clean_sdist:
	- rm -rf dist

clean: 
	- make clean_develop 
	- make clean_pypi

pypi: clean clean_sdist
	set -x \
	&& $(python) setup.py sdist bdist_wheel \
	&& twine check dist/* \
	&& twine upload dist/*

clean_pypi:
	- rm -rf build/

conda_update:
	- conda update --all -y
	- pip freeze > ./requirements.txt
	- conda env export | cut -f 1 -d '=' | grep -v "prefix" > ./requirements.yml

conda_export:
	- pip freeze > ./requirements.txt
	- conda env export | cut -f 1 -d '=' | grep -v "prefix" > ./requirements.yml
SHELL=bash
python=python
pip=pip
tests=.
version:=$(shell $(python) version.py)
sdist_name:=SplatStats-$(version).tar.gz


###############################################################################
# Dev
###############################################################################
develop:
	$(pip) install -e .

clean_develop:
	- $(pip) uninstall -y SplatStats
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
	&& twine upload dist/* \
	&& pip install .

clean_pypi:
	- rm -rf build/

doc:
	- python -m pip install .
	- sphinx-apidoc -f -o docs/source SplatStats
	- sphinx-build -b html docs/source/ docs/build/html

###############################################################################
# Conda
###############################################################################
conda_update:
	- conda update --all -y
	- pip freeze > ./requirements.txt
	- conda env export | cut -f 1 -d '=' | grep -v "prefix" > ./requirements.yml

conda_export:
	- pip freeze > ./requirements.txt
	- conda env export | cut -f 1 -d '=' | grep -v "prefix" > ./requirements.yml

###############################################################################
# Docker SplatStats
###############################################################################
docker_build:
	- docker rmi splatstats:dev -f
	- docker build -f Dockerfile.splatstats -t splatstats:dev .

docker_build_force:
	- docker rmi splatstats:dev -f
	- docker build -f Dockerfile.splatstats --no-cache -t splatstats:dev .

docker_run:
	- docker run --mount type=bind,source=${PWD},target=/data splatstats:dev  --download "True" --upload "True" --player 'čħîþ ウナギ'

docker_run_python:
	- docker run -it splatstats:dev python

docker_run_bash:
	- docker run -it --entrypoint /bin/bash splatstats:dev

docker_exec:
	- docker run --mount type=bind,source=${PWD},target=/data -it splatstats:dev bash

docker_release:
	- docker buildx build -f Dockerfile.splatstats .\
		--platform=linux/amd64,linux/arm64,linux/x86_64 \
		-t chipdelmal/splatstats:$(version) \
		-t chipdelmal/splatstats:latest \
		--push

###############################################################################
# Docker InkStats
###############################################################################
docker_build_ink:
	- docker rmi inkstats:dev -f
	- docker build -f Dockerfile.inkstats -t inkstats:dev .

docker_build_force_ink:
	- docker rmi inkstats:dev -f
	- docker build -f Dockerfile.inkstats --no-cache -t inkstats:dev .

docker_run_ink:
	- docker run --mount type=bind,source=${PWD},target=/data inkstats:dev --season "All" --titles "True" --gmode 'All' --overwrite 'False' --dpi '500'

docker_run_python_ink:
	- docker run -it inkstats:dev python

docker_run_bash_ink:
	- docker run -it --entrypoint /bin/bash inkstats:dev

docker_exec_ink:
	- docker run --mount type=bind,source=${PWD},target=/data -it inkstats:dev bash

docker_release_ink:
	- docker buildx build -f Dockerfile.inkstats .\
		--platform=linux/amd64,linux/arm64,linux/x86_64 \
		-t chipdelmal/inkstats:$(version) \
		-t chipdelmal/inkstats:latest \
		--push
 
###############################################################################
# Full version release
###############################################################################
full_release:
	- make pypi
	- make docker_release
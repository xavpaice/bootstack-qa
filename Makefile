PROJECTPATH=$(dir $(realpath $(MAKEFILE_LIST)))
CHARM_BUILD_DIR=${PROJECTPATH}.build


submodules:
	@echo "Cloning submodules"
	@git submodule update --init --recursive

submodules-update:
	@echo "Pulling latest updates for submodules"
	@git submodule update --init --recursive --remote --merge

builds: submodules submodules-update
	@cd lib/graylog ; make build

functional: builds
	tox -e func

smoke: builds
	tox -e smoke

clean:
	@rm -rf .tox .build/*

.PHONY: submodules submodules-update builds functional clean

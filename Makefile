PROJECTPATH=$(dir $(realpath $(MAKEFILE_LIST)))
ifndef CHARM_BUILD_DIR
	CHARM_BUILD_DIR=${PROJECTPATH}.build
endif


submodules:
	@echo "Cloning submodules"
	@git submodule update --init --recursive

submodules-update:
	@echo "Pulling latest updates for submodules"
	@git submodule update --init --recursive --remote --merge

builds: submodules submodules-update
	@cd mod/graylog ; make build

functional: builds
	tox -e func

clean:
	@rm -rf .tox .build/*

.PHONY: submodules submodules-update builds functional clean

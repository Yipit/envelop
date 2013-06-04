# Variables you might need to change in the first place
#
# This is probably the only section you'll need to change in this Makefile.
# Also, make sure you don't remove the `<variables/>' tag. Cause those marks
# are going to be used to update this file automatically.
#
# <variables>
PACKAGE=handy
CUSTOM_PIP_INDEX=localshop
# </variables>

all: unit functional integration acceptance steadymark

unit:
	@make run_test suite=unit

functional:
	@make run_test suite=functional

integration:
	@make run_test suite=integration

acceptance:
	@if hash lettuce 2>/dev/null; then \
		lettuce; \
	fi

steadymark:
	@if hash steadymark 2>/dev/null; then \
		steadymark; \
	fi

prepare: clean install_deps

run_test:
	@if [ -d tests/$(suite) ]; then \
		echo "Running \033[0;32m$(suite)\033[0m test suite"; \
		make prepare && \
			nosetests --rednose --stop \
				--with-coverage --cover-package=$(PACKAGE) --cover-branches \
				--verbosity=2 -s tests/$(suite) ; \
	fi

install_deps:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "You're not running this from a virtualenv, wtf dude?"; \
		exit 1; \
	fi

	@if [ -z $$SKIP_DEPS ]; then \
		echo "Installing missing dependencies..."; \
		[ -e development.txt  ] && pip install -r development.txt; \
	fi

	@python setup.py develop &> .build.log

clean:
	@echo "Removing garbage..."
	@find . -name '*.pyc' -delete
	@find . -name '*.so' -delete
	@find . -name __pycache__ -delete
	@rm -rf .coverage *.egg-info *.log build dist MANIFEST

publish:
	@if [ -e "$$HOME/.pypirc" ]; then \
		echo "Uploading to '$(CUSTOM_PIP_INDEX)'"; \
		python setup.py register -r "$(CUSTOM_PIP_INDEX)"; \
		python setup.py sdist upload -r "$(CUSTOM_PIP_INDEX)"; \
	else \
		echo "You should create a file called \`.pypirc' under your home dir.\n"; \
		echo "That's the right place to configure \`pypi' repos.\n"; \
		echo "Read more about it here: https://github.com/Yipit/yipit/blob/dev/docs/rfc/RFC00007-python-packages.md"; \
		exit 1; \
	fi

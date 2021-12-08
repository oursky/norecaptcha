.PHONY: check
check:
	black . --check

.PHONY: build
build:
	python3 -m build --sdist

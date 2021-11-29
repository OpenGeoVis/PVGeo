# Simple makefile to simplify repetitive build env management tasks under posix

CODESPELL_DIRS ?= ./
CODESPELL_SKIP ?= "*.pyc,*.txt,*.gif,*.png,*.jpg,*.ply,*.vtk,*.vti,*.js,*.html,*.doctree,*.ttf,*.woff,*.woff2,*.eot,*.mp4,*.inv,*.pickle,*.css,*.json,*.ipynb,flycheck*,./.git/*,./.hypothesis/*,*.yml,./doc/_build/*,./doc/images/*,./dist/*,*~,.hypothesis*,./doc/source/examples/*,*.mypy_cache/*,*cover,./tests/tinypages/_build/*,*/_autosummary/*,htmlcov/"
CODESPELL_IGNORE ?= "ignore_words.txt"


stylecheck: codespell lint

codespell:
	@echo "Running codespell"
	@codespell $(CODESPELL_DIRS) -S $(CODESPELL_SKIP)

pydocstyle:
	@echo "Running pydocstyle"
	@pydocstyle PVGeo --match='(?!coverage).*.py'

doctest:
	@echo "Runnnig module doctesting"
	pytest -v --doctest-modules PVGeo

lint:
	@echo "Linting with flake8"
	flake8 .

format:
	@echo "Formatting"
	black .
	isort .

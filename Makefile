.PHONY: build
build: dist/t3

dist/t3: dist/requirements.txt
	uvx pex \
	        -r dist/requirements.txt \
			--sources=src/ \
			-m t3.cli \
            --scie eager \
            --scie-pbs-stripped \
            -o dist/t3.pex

dist/requirements.txt:
	uv pip compile pyproject.toml -o dist/requirements.txt

.PHONY: clean
clean:
	rm -rf dist src/t3.egg-info
	find src -type f -name *.pyc -delete
	find src -type d -name __pycache__ -delete

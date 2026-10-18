all: myegrep

myegrep:
	@echo '#!/bin/sh' > myegrep
	@echo 'DIR=$$(dirname "$$0")' >> myegrep
	@echo 'PYTHONPATH="$$DIR" exec python3 -m src.myegrep "$$@"' >> myegrep
	@chmod +x myegrep

test:
	python3 -m pytest tests/ -v

clean:
	rm -f myegrep

.PHONY: all test clean

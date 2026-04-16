.PHONY: setup

setup:
	-@docker rm -f empathetic-mongo >/dev/null 2>&1 || true
	@docker run -d --name empathetic-mongo -p 27017:27017 mongo:7 >/dev/null
	@echo "MongoDB running at mongodb://localhost:27017"

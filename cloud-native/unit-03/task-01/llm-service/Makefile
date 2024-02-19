.PHONY: wheel create-image push run
wheel: src/*
	pip wheel src/ -w dist/

push: wheel docker/Dockerfile
	docker buildx build --push --tag cyberphorwashere.azurecr.io/llmservice:latest -f docker/Dockerfile  . 



run: create-image
	docker run -p 8080:8080 worker:latest


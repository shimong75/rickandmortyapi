APP_NAME := rickandmorty
DOCKER_REPO := localhost:5000
PORT := 8080
# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help


run_locally: ## run locally on host (without docker)
	pip install -r requirements.txt
	python app.py

# DOCKER TASKS
# Build the container
build: ## Build the image
	docker build -t $(APP_NAME) .

build-nc: ## Build the image without caching
	docker build --no-cache -t $(APP_NAME) .

run: ## Run container on port configured in `config.env`
	docker run --rm -p=$(PORT):$(PORT) --name="$(APP_NAME)" $(APP_NAME)

up: build run ## Run container on port configured in `config.env` (Alias to run)


stop: ## Stop and remove a running container
	docker stop $(APP_NAME); docker rm $(APP_NAME)


minikube_build: eval_docekr_env ## build docker in minikube env
	docker build -t  $(DOCKER_REPO)/$(APP_NAME) .


minikube_build_nc: eval_docekr_env ## build docker in minikube env
	docker build --no-cache -t $(DOCKER_REPO)/$(APP_NAME) .


minikube_push: eval_docekr_env ## push the app image to minikube registry
	docker push  $(DOCKER_REPO)/$(APP_NAME)


minikube_up: minikube_build_nc minikube_push eval_docekr_env ## deploy the app on k8s (minikube cluster)
	kubectl apply -f yamls/

minikube_clear:  eval_docekr_env ## clear the minikube cluster from the app resources
	kubectl delete -f yamls


eval_docekr_env: ## sets shell to docker env of minikube
	@eval $$(minikube docker-env)


clean_etc_hosts: ## clear the etc/hosts from the minikube created previously (works only on mac)
	sudo sed  -i '' '/rickandmorty/d'  /etc/hosts



## Usage examples

hc: ## health check local env
	curl "localhost:5000/healthcheck"

fetch_all: ## fetch all from minikubegit
	curl "localhost:5000/all"

fetch_by_name_example: ## fetch specific name example
	curl 'localhost:5000/characters?name=Veterinary%20Nurse&name=Tricia%20Lange'

fetch_by_location_example: ## fetch all characters from location
	curl "localhost:5000/locations?location=Earth%20(Replacement%20Dimension)"


minikube_hc: ## health check minikube
	curl "rickandmorty.info/healthcheck"

minikube_fetch_all: ## fetch all from minikube
	curl "rickandmorty.info/all"

minikube_follow_logs: ## follow the logs of the app
	kubectl logs --follow $$(kubectl get pods -l app=rickandmorty --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')

minikube_fetch_by_name_example: ## fetch specific name example
	curl 'localhost:5000/characters?name=Veterinary%20Nurse&name=Tricia%20Lange'

minikube_fetch_by_location_example: ## fetch all characters from location
	curl "localhost:5000/locations?location=Earth%20(Replacement%20Dimension)"


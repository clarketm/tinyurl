-include Makefile.common.mk

.PHONY: hooks precommit
hooks precommit:
	@cp -f ./hooks/pre-commit $(shell  git rev-parse --git-path hooks)

.PHONY: hash
hash:
	@mkdir -p ./config
	@git rev-parse --short=7 HEAD > ./config/BUILD

.PHONY: start
start:
	@docker-compose up

.PHONY: start-dev
start-dev:
	@docker-compose -f docker-compose.dev.yml up

.PHONY: deploy-new
deploy-new:
	# Install nginx-ingress
	@kubectl create namespace nginx-ingress
	@helm install nginx-ingress stable/nginx-ingress --namespace nginx-ingress
	# Install cert-manager
	@kubectl create namespace cert-manager
	@kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v0.14.1/cert-manager.crds.yaml
	@helm install cert-manager jetstack/cert-manager --namespace cert-manager
	# Install tinyurl
	@kubectl create namespace app
	@helm install tinyurl ./deploy --namespace app

.PHONY: deploy-update
deploy-update:
	@helm upgrade tinyurl ./deploy --namespace app

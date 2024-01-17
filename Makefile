all: lint deploy test

init: # installs rbac-manager on the cluster
	helm repo add fairwinds-stable https://charts.fairwinds.com/stable
	helm install rbac-manager fairwinds-stable/rbac-manager --namespace rbac-manager --create-namespace

lint:
	helm lint rbacdefinitions

deploy:
	helm upgrade --install rbacdefinitions rbacdefinitions

test:
	helm test rbacdefinitions

destroy:
	helm uninstall rbacdefinitions

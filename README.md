# Description

This is a simple project to demonstrate how to deploy rbac-manager rbacdefintions in a cluster via helm and then run policy checks against them.

## Prerequisites

* Install [Helm](https://helm.sh/docs/intro/install/)
* Connect to a Kubernetes cluster

## Instructions

### Deploy rbac-manager

```bash
make init
```

### Deploy rbacdefintions

```bash
make deploy
```

You can edit rbacdefintions in `rbacdefinitions/templates/rbac-defintion.yaml`.

### Run policy checks

```bash
make test
```

You can edit the policy tests in `rbacdefinitions/integration-tests/test_policies.py`.

### Cleanup

```bash
make destroy # destroys the rbacdefitions
```


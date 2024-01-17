from kubernetes import client, config
import pytest
from typing import NamedTuple

@pytest.fixture(scope="module")
def k8s_auth_client():
    config.load_incluster_config()
    return client.AuthorizationV1Api()

class PolicyTest(NamedTuple):
    allowed: bool # determines whether the specified policy details should be allowed when running the test
    verb: str = "*" # the action verb to test (defaults to *)
    resource: str = "*" # the resource to check (defaults to *)
    namespace: str = "" # "" means all
    group: str = "*" # defaults to all groups


TESTS = [
    # Readonly group should be able to to list pods operations in all namespaces
    PolicyTest(allowed=True, verb="list", resource="pods", group="readonlygroup"),
    
    # Readonly group should not be able to list secrets
    PolicyTest(allowed=False, verb="list", resource="secrets", group="readonlygroup"),
    
    # Readonly group should not be able to list secrets
    PolicyTest(allowed=False, verb="list", resource="secrets", group="readonlygroup"),
    
    # Developer group should be able to list secrets in default namespace 
    PolicyTest(allowed=True, verb="list", resource="secrets", group="developergroup", namespace="default"),
    
    # Developer group should not be able to list secrets in kube-system namespace
    PolicyTest(allowed=False, verb="list", resource="secrets", group="developergroup", namespace="kube-system"),

    # Admin group should be able to create secretes in kube-system namespace
    PolicyTest(allowed=True, verb="delete", resource="secrets", group="admin", namespace="kube-system"),
]

@pytest.mark.parametrize("policy_test", TESTS)
def test_policies(k8s_auth_client: client.AuthorizationApi, policy_test: PolicyTest):
    
    subject_access_review_spec = client.V1SubjectAccessReviewSpec(
        groups=[policy_test.group],
        resource_attributes=client.V1ResourceAttributes(
            verb=policy_test.verb,
            resource=policy_test.resource,
            namespace=policy_test.namespace
        )
    )

    body = client.V1SubjectAccessReview(spec=subject_access_review_spec)

    response: client.V1SubjectAccessReview = k8s_auth_client.create_subject_access_review(
        body=body
    )

    assert response.status.allowed is policy_test.allowed, response.status

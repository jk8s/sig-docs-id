diff --git a/content/en/docs/concepts/security/overview.md b/content/en/docs/concepts/security/overview.md
index 98776c719..fe9129c10 100644
--- a/content/en/docs/concepts/security/overview.md
+++ b/content/en/docs/concepts/security/overview.md
@@ -103,7 +103,7 @@ areas of security concerns and recommendations for securing workloads running in
 Area of Concern for Workload Security | Recommendation |
 ------------------------------ | --------------------- |
 RBAC Authorization (Access to the Kubernetes API) | https://kubernetes.io/docs/reference/access-authn-authz/rbac/
-Authentication | https://kubernetes.io/docs/reference/access-authn-authz/controlling-access/
+Authentication | https://kubernetes.io/docs/concepts/security/controlling-access/
 Application secrets management (and encrypting them in etcd at rest) | https://kubernetes.io/docs/concepts/configuration/secret/ <br> https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/
 Pod Security Policies | https://kubernetes.io/docs/concepts/policy/pod-security-policy/
 Quality of Service (and Cluster resource management) | https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/
@@ -147,8 +147,8 @@ Learn about related Kubernetes security topics:
 
 * [Pod security standards](/docs/concepts/security/pod-security-standards/)
 * [Network policies for Pods](/docs/concepts/services-networking/network-policies/)
+* [Controlling Access to the Kubernetes API](/docs/concepts/security/controlling-access)
 * [Securing your cluster](/docs/tasks/administer-cluster/securing-a-cluster/)
-* [API access control](/docs/reference/access-authn-authz/controlling-access/)
 * [Data encryption in transit](/docs/tasks/tls/managing-tls-in-a-cluster/) for the control plane
 * [Data encryption at rest](/docs/tasks/administer-cluster/encrypt-data/)
 * [Secrets in Kubernetes](/docs/concepts/configuration/secret/)


diff --git a/content/en/docs/reference/access-authn-authz/_index.md b/content/en/docs/reference/access-authn-authz/_index.md
index 4e1bff081..d999e52bf 100644
--- a/content/en/docs/reference/access-authn-authz/_index.md
+++ b/content/en/docs/reference/access-authn-authz/_index.md
@@ -1,4 +1,26 @@
 ---
-title: Accessing the API
+title: API Access Control
 weight: 20
----
\ No newline at end of file
+no_list: true
+---
+
+For an introduction to how Kubernetes implements and controls API access,
+read [Controlling Access to the Kubernetes API](/docs/concepts/security/controlling-access/).
+
+Reference documentation:
+
+- [Authenticating](/docs/reference/access-authn-authz/authentication/)
+   - [Authenticating with Bootstrap Tokens](/docs/reference/access-authn-authz/bootstrap-tokens/)
+- [Admission Controllers](/docs/reference/access-authn-authz/admission-controllers/)
+   - [Dynamic Admission Control](/docs/reference/access-authn-authz/extensible-admission-controllers/)
+- [Authorization](/docs/reference/access-authn-authz/authorization/)
+   - [Role Based Access Control](/docs/reference/access-authn-authz/rbac/)
+   - [Attribute Based Access Control](/docs/reference/access-authn-authz/abac/)
+   - [Node Authorization](/docs/reference/access-authn-authz/node/)
+   - [Webhook Authorization](/docs/reference/access-authn-authz/webhook/)
+- [Certificate Signing Requests](/docs/reference/access-authn-authz/certificate-signing-requests/)
+   - including [CSR approval](/docs/reference/access-authn-authz/certificate-signing-requests/#approval-rejection)
+     and [certificate signing](/docs/reference/access-authn-authz/certificate-signing-requests/#signing)
+- Service accounts
+  - [Developer guide](/docs/tasks/configure-pod-container/configure-service-account/)
+  - [Administration](/docs/reference/access-authn-authz/service-accounts-admin/)


diff --git a/content/en/docs/tasks/configure-pod-container/configure-service-account.md b/content/en/docs/tasks/configure-pod-container/configure-service-account.md
index 2486e520e..e3f97dd5c 100644
--- a/content/en/docs/tasks/configure-pod-container/configure-service-account.md
+++ b/content/en/docs/tasks/configure-pod-container/configure-service-account.md
@@ -39,10 +39,14 @@ When they do, they are authenticated as a particular Service Account (for exampl
 
 When you create a pod, if you do not specify a service account, it is
 automatically assigned the `default` service account in the same namespace.
-If you get the raw json or yaml for a pod you have created (for example, `kubectl get pods/<podname> -o yaml`), you can see the `spec.serviceAccountName` field has been [automatically set](/docs/user-guide/working-with-resources/#resources-are-automatically-modified).
+If you get the raw json or yaml for a pod you have created (for example, `kubectl get pods/<podname> -o yaml`),
+you can see the `spec.serviceAccountName` field has been
+[automatically set](/docs/concepts/overview/working-with-objects/object-management/).
 
-You can access the API from inside a pod using automatically mounted service account credentials, as described in [Accessing the Cluster](/docs/user-guide/accessing-the-cluster/#accessing-the-api-from-a-pod).
-The API permissions of the service account depend on the [authorization plugin and policy](/docs/reference/access-authn-authz/authorization/#authorization-modules) in use.
+You can access the API from inside a pod using automatically mounted service account credentials, as described in
+[Accessing the Cluster](/docs/tasks/access-application-cluster/access-cluster).
+The API permissions of the service account depend on the
+[authorization plugin and policy](/docs/reference/access-authn-authz/authorization/#authorization-modules) in use.
 
 In version 1.6+, you can opt out of automounting API credentials for a service account by setting `automountServiceAccountToken: false` on the service account:
 
@@ -316,7 +320,7 @@ kubectl create -f https://k8s.io/examples/pods/pod-projected-svc-token.yaml
 The kubelet will request and store the token on behalf of the pod, make the
 token available to the pod at a configurable file path, and refresh the token as it approaches expiration. Kubelet proactively rotates the token if it is older than 80% of its total TTL, or if the token is older than 24 hours.
 
-The application is responsible for reloading the token when it rotates. Periodic reloading (e.g. once every 5 minutes) is sufficient for most usecases.
+The application is responsible for reloading the token when it rotates. Periodic reloading (e.g. once every 5 minutes) is sufficient for most use cases.
 
 ## Service Account Issuer Discovery
 


diff --git a/content/en/docs/tutorials/stateless-application/expose-external-ip-address.md b/content/en/docs/tutorials/stateless-application/expose-external-ip-address.md
index 2974c77c9..5babc2c0b 100644
--- a/content/en/docs/tutorials/stateless-application/expose-external-ip-address.md
+++ b/content/en/docs/tutorials/stateless-application/expose-external-ip-address.md
@@ -52,11 +52,11 @@ kubectl apply -f https://k8s.io/examples/service/load-balancer-example.yaml
 
 
 The preceding command creates a
-    [Deployment](/docs/concepts/workloads/controllers/deployment/)
-    object and an associated
-    [ReplicaSet](/docs/concepts/workloads/controllers/replicaset/)
-    object. The ReplicaSet has five
-    [Pods](/docs/concepts/workloads/pods/pod/),
+    {{< glossary_tooltip text="Deployment" term_id="deployment" >}}
+    and an associated
+    {{< glossary_tooltip term_id="replica-set" text="ReplicaSet" >}}.
+    The ReplicaSet has five
+    {{< glossary_tooltip text="Pods" term_id="pod" >}}
     each of which runs the Hello World application.
 
 1. Display information about the Deployment:


diff --git a/content/en/docs/concepts/services-networking/_index.md b/content/en/docs/concepts/services-networking/_index.md
index eea2c65b3..2e7d91427 100755
--- a/content/en/docs/concepts/services-networking/_index.md
+++ b/content/en/docs/concepts/services-networking/_index.md
@@ -1,5 +1,12 @@
 ---
 title: "Services, Load Balancing, and Networking"
 weight: 60
+description: >
+  Concepts and resources behind networking in Kubernetes.
 ---
 
+Kubernetes networking addresses four concerns:
+- Containers within a Pod use networking to communicate via loopback.
+- Cluster networking provides communication between different Pods.
+- The Service resource lets you expose an application running in Pods to be reachable from outside your cluster.
+- You can also use Services to publish services only for consumption inside your cluster.


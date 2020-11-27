diff --git a/content/en/docs/tasks/configure-pod-container/configure-persistent-volume-storage.md b/content/en/docs/tasks/configure-pod-container/configure-persistent-volume-storage.md
index 6ff6c2153..a53d27822 100644
--- a/content/en/docs/tasks/configure-pod-container/configure-persistent-volume-storage.md
+++ b/content/en/docs/tasks/configure-pod-container/configure-persistent-volume-storage.md
@@ -29,13 +29,11 @@ PersistentVolume.
 {{< glossary_tooltip text="kubectl" term_id="kubectl" >}}
 command-line tool must be configured to communicate with your cluster. If you
 do not already have a single-node cluster, you can create one by using
-[Minikube](/docs/getting-started-guides/minikube).
+[Minikube](https://minikube.sigs.k8s.io/docs/).
 
 * Familiarize yourself with the material in
 [Persistent Volumes](/docs/concepts/storage/persistent-volumes/).
 
-
-
 <!-- steps -->
 
 ## Create an index.html file on your Node
@@ -262,8 +260,8 @@ metadata:
 ```
 When a Pod consumes a PersistentVolume that has a GID annotation, the annotated GID
 is applied to all containers in the Pod in the same way that GIDs specified in the
-Pod’s security context are. Every GID, whether it originates from a PersistentVolume
-annotation or the Pod’s specification, is applied to the first process run in
+Pod's security context are. Every GID, whether it originates from a PersistentVolume
+annotation or the Pod's specification, is applied to the first process run in
 each container.
 
 {{< note >}}


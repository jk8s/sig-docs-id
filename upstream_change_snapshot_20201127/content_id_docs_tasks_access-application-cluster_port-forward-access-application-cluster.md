diff --git a/content/en/docs/tasks/access-application-cluster/port-forward-access-application-cluster.md b/content/en/docs/tasks/access-application-cluster/port-forward-access-application-cluster.md
index a6c2e217a..3eceb4f6d 100644
--- a/content/en/docs/tasks/access-application-cluster/port-forward-access-application-cluster.md
+++ b/content/en/docs/tasks/access-application-cluster/port-forward-access-application-cluster.md
@@ -152,7 +152,7 @@ for database debugging.
     or
 
     ```shell
-    kubectl port-forward service/redis-master 7000:6379
+    kubectl port-forward service/redis-master 7000:redis
     ```
 
     Any of the above commands works. The output is similar to this:


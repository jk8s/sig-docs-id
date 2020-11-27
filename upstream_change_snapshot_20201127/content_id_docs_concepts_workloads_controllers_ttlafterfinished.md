diff --git a/content/en/docs/concepts/workloads/controllers/ttlafterfinished.md b/content/en/docs/concepts/workloads/controllers/ttlafterfinished.md
index 3a43d5e7b..6b6ad65e0 100644
--- a/content/en/docs/concepts/workloads/controllers/ttlafterfinished.md
+++ b/content/en/docs/concepts/workloads/controllers/ttlafterfinished.md
@@ -20,12 +20,6 @@ Alpha Disclaimer: this feature is currently alpha, and can be enabled with both
 [feature gate](/docs/reference/command-line-tools-reference/feature-gates/)
 `TTLAfterFinished`.
 
-
-
-
-
-
-
 <!-- body -->
 
 ## TTL Controller
@@ -82,9 +76,7 @@ very small. Please be aware of this risk when setting a non-zero TTL.
 
 ## {{% heading "whatsnext" %}}
 
+* [Clean up Jobs automatically](/docs/concepts/workloads/controllers/job/#clean-up-finished-jobs-automatically)
 
-[Clean up Jobs automatically](/docs/concepts/workloads/controllers/jobs-run-to-completion/#clean-up-finished-jobs-automatically)
-
-[Design doc](https://github.com/kubernetes/enhancements/blob/master/keps/sig-apps/0026-ttl-after-finish.md)
-
+* [Design doc](https://github.com/kubernetes/enhancements/blob/master/keps/sig-apps/0026-ttl-after-finish.md)
 


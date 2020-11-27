diff --git a/content/en/docs/tasks/administer-cluster/namespaces.md b/content/en/docs/tasks/administer-cluster/namespaces.md
index eabf58ff0..00dec4177 100644
--- a/content/en/docs/tasks/administer-cluster/namespaces.md
+++ b/content/en/docs/tasks/administer-cluster/namespaces.md
@@ -13,7 +13,7 @@ This page shows how to view, work in, and delete {{< glossary_tooltip text="name
 ## {{% heading "prerequisites" %}}
 
 * Have an [existing Kubernetes cluster](/docs/setup/).
-* Have a basic understanding of Kubernetes _[Pods](/docs/concepts/workloads/pods/pod/)_, _[Services](/docs/concepts/services-networking/service/)_, and _[Deployments](/docs/concepts/workloads/controllers/deployment/)_.
+2. You have a basic understanding of Kubernetes {{< glossary_tooltip text="Pods" term_id="pod" >}}, {{< glossary_tooltip term_id="service" text="Services" >}}, and {{< glossary_tooltip text="Deployments" term_id="deployment" >}}.
 
 
 <!-- steps -->
@@ -194,8 +194,7 @@ This delete is asynchronous, so for a time you will see the namespace in the `Te
     To demonstrate this, let's spin up a simple Deployment and Pods in the `development` namespace.
 
     ```shell
-    kubectl create deployment snowflake --image=k8s.gcr.io/serve_hostname -n=development
-    kubectl scale deployment snowflake --replicas=2 -n=development
+    kubectl create deployment snowflake --image=k8s.gcr.io/serve_hostname  -n=development --replicas=2
     ```
     We have just created a deployment whose replica size is 2 that is running the pod called `snowflake` with a basic container that just serves the hostname.
 


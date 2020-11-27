diff --git a/content/en/docs/tasks/run-application/run-stateless-application-deployment.md b/content/en/docs/tasks/run-application/run-stateless-application-deployment.md
index 9e6ed4a25..df604facf 100644
--- a/content/en/docs/tasks/run-application/run-stateless-application-deployment.md
+++ b/content/en/docs/tasks/run-application/run-stateless-application-deployment.md
@@ -80,7 +80,7 @@ a Deployment that runs the nginx:1.14.2 Docker image:
         NewReplicaSet:    nginx-deployment-1771418926 (2/2 replicas created)
         No events.
 
-1. List the pods created by the deployment:
+1. List the Pods created by the deployment:
 
         kubectl get pods -l app=nginx
 
@@ -113,9 +113,9 @@ specifies that the deployment should be updated to use nginx 1.16.1.
 
 ## Scaling the application by increasing the replica count
 
-You can increase the number of pods in your Deployment by applying a new YAML
+You can increase the number of Pods in your Deployment by applying a new YAML
 file. This YAML file sets `replicas` to 4, which specifies that the Deployment
-should have four pods:
+should have four Pods:
 
 {{< codenew file="application/deployment-scale.yaml" >}}
 
@@ -123,7 +123,7 @@ should have four pods:
 
         kubectl apply -f https://k8s.io/examples/application/deployment-scale.yaml
 
-1. Verify that the Deployment has four pods:
+1. Verify that the Deployment has four Pods:
 
         kubectl get pods -l app=nginx
 


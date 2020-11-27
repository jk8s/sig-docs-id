diff --git a/content/en/docs/concepts/cluster-administration/manage-deployment.md b/content/en/docs/concepts/cluster-administration/manage-deployment.md
index b052dd3a1..50ed69ff4 100644
--- a/content/en/docs/concepts/cluster-administration/manage-deployment.md
+++ b/content/en/docs/concepts/cluster-administration/manage-deployment.md
@@ -10,9 +10,6 @@ weight: 40
 
 You've deployed your application and exposed it via a service. Now what? Kubernetes provides a number of tools to help you manage your application deployment, including scaling and updating. Among the features that we will discuss in more depth are [configuration files](/docs/concepts/configuration/overview/) and [labels](/docs/concepts/overview/working-with-objects/labels/).
 
-
-
-
 <!-- body -->
 
 ## Organizing resource configurations
@@ -323,7 +320,7 @@ When load on your application grows or shrinks, it's easy to scale with `kubectl
 kubectl scale deployment/my-nginx --replicas=1
 ```
 ```shell
-deployment.extensions/my-nginx scaled
+deployment.apps/my-nginx scaled
 ```
 
 Now you only have one pod managed by the deployment.
@@ -356,7 +353,8 @@ Sometimes it's necessary to make narrow, non-disruptive updates to resources you
 
 ### kubectl apply
 
-It is suggested to maintain a set of configuration files in source control (see [configuration as code](http://martinfowler.com/bliki/InfrastructureAsCode.html)),
+It is suggested to maintain a set of configuration files in source control
+(see [configuration as code](https://martinfowler.com/bliki/InfrastructureAsCode.html)),
 so that they can be maintained and versioned along with the code for the resources they configure.
 Then, you can use [`kubectl apply`](/docs/reference/generated/kubectl/kubectl-commands/#apply) to push your configuration changes to the cluster.
 


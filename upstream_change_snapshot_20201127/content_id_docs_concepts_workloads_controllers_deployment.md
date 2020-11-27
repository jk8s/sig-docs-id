diff --git a/content/en/docs/concepts/workloads/controllers/deployment.md b/content/en/docs/concepts/workloads/controllers/deployment.md
index 5e7374d5c..54448de92 100644
--- a/content/en/docs/concepts/workloads/controllers/deployment.md
+++ b/content/en/docs/concepts/workloads/controllers/deployment.md
@@ -13,7 +13,7 @@ weight: 10
 
 <!-- overview -->
 
-A _Deployment_ provides declarative updates for {{< glossary_tooltip text="Pods" term_id="pod" >}}
+A _Deployment_ provides declarative updates for {{< glossary_tooltip text="Pods" term_id="pod" >}} and
 {{< glossary_tooltip term_id="replica-set" text="ReplicaSets" >}}.
 
 You describe a _desired state_ in a Deployment, and the Deployment {{< glossary_tooltip term_id="controller" >}} changes the actual state to the desired state at a controlled rate. You can define Deployments to create new ReplicaSets, or to remove existing Deployments and adopt all their resources with new Deployments.
@@ -752,7 +752,7 @@ apply multiple fixes in between pausing and resuming without triggering unnecess
     REVISION  CHANGE-CAUSE
     1   <none>
     ```
-* Get the rollout status to ensure that the Deployment is updates successfully:
+* Get the rollout status to ensure that the Deployment is updated successfully:
     ```shell
     kubectl get rs
     ```


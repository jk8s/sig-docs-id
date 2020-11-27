diff --git a/content/en/docs/concepts/configuration/pod-priority-preemption.md b/content/en/docs/concepts/configuration/pod-priority-preemption.md
index 10a054cfa..d6acc80a7 100644
--- a/content/en/docs/concepts/configuration/pod-priority-preemption.md
+++ b/content/en/docs/concepts/configuration/pod-priority-preemption.md
@@ -321,9 +321,7 @@ Pod may be created that fits on the same Node. In this case, the scheduler will
 schedule the higher priority Pod instead of the preemptor.
 
 This is expected behavior: the Pod with the higher priority should take the place
-of a Pod with a lower priority. Other controller actions, such as
-[cluster autoscaling](/docs/tasks/administer-cluster/cluster-management/#cluster-autoscaling),
-may eventually provide capacity to schedule the pending Pods.
+of a Pod with a lower priority.
 
 ### Higher priority Pods are preempted before lower priority pods
 


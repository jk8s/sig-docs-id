diff --git a/content/en/docs/concepts/services-networking/service.md b/content/en/docs/concepts/services-networking/service.md
index ded1451d8..83b785036 100644
--- a/content/en/docs/concepts/services-networking/service.md
+++ b/content/en/docs/concepts/services-networking/service.md
@@ -881,6 +881,10 @@ There are other annotations to manage Classic Elastic Load Balancers that are de
         # health check. This value must be less than the service.beta.kubernetes.io/aws-load-balancer-healthcheck-interval
         # value. Defaults to 5, must be between 2 and 60
 
+        service.beta.kubernetes.io/aws-load-balancer-security-groups: "sg-53fae93f"
+        # A list of existing security groups to be added to ELB created. Unlike the annotation
+        # service.beta.kubernetes.io/aws-load-balancer-extra-security-groups, this replaces all other security groups previously assigned to the ELB.
+
         service.beta.kubernetes.io/aws-load-balancer-extra-security-groups: "sg-53fae93f,sg-42efd82e"
         # A list of additional security groups to be added to the ELB
 


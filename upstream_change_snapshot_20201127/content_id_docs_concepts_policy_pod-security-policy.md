diff --git a/content/en/docs/concepts/policy/pod-security-policy.md b/content/en/docs/concepts/policy/pod-security-policy.md
index 5a5241c42..299d681d1 100644
--- a/content/en/docs/concepts/policy/pod-security-policy.md
+++ b/content/en/docs/concepts/policy/pod-security-policy.md
@@ -14,9 +14,6 @@ weight: 20
 Pod Security Policies enable fine-grained authorization of pod creation and
 updates.
 
-
-
-
 <!-- body -->
 
 ## What is a Pod Security Policy?
@@ -143,13 +140,17 @@ For a complete example of authorizing a PodSecurityPolicy, see
 
 ### Troubleshooting
 
-- The [Controller Manager](/docs/admin/kube-controller-manager/) must be run
-against [the secured API port](/docs/reference/access-authn-authz/controlling-access/),
-and must not have superuser permissions. Otherwise requests would bypass
-authentication and authorization modules, all PodSecurityPolicy objects would be
-allowed, and users would be able to create privileged containers. For more details
-on configuring Controller Manager authorization, see [Controller
-Roles](/docs/reference/access-authn-authz/rbac/#controller-roles).
+- The [controller manager](/docs/reference/command-line-tools-reference/kube-controller-manager/)
+  must be run against the secured API port and must not have superuser permissions. See
+  [Controlling Access to the Kubernetes API](/docs/concepts/security/controlling-access)
+  to learn about API server access controls.  
+  If the controller manager connected through the trusted API port (also known as the
+  `localhost` listener), requests would bypass authentication and authorization modules;
+  all PodSecurityPolicy objects would be allowed, and users would be able to create grant
+  themselves the ability to create privileged containers.
+
+  For more details on configuring controller manager authorization, see
+  [Controller Roles](/docs/reference/access-authn-authz/rbac/#controller-roles).
 
 ## Policy Order
 
@@ -302,7 +303,7 @@ kubectl-user delete pod pause
 Let's try that again, slightly differently:
 
 ```shell
-kubectl-user run pause --image=k8s.gcr.io/pause
+kubectl-user create deployment pause --image=k8s.gcr.io/pause
 deployment "pause" created
 
 kubectl-user get pods
@@ -599,8 +600,11 @@ documentation](/docs/tutorials/clusters/apparmor/#podsecuritypolicy-annotations)
 
 ### Seccomp
 
-The use of seccomp profiles in pods can be controlled via annotations on the
-PodSecurityPolicy. Seccomp is an alpha feature in Kubernetes.
+As of Kubernetes v1.19, you can use the `seccompProfile` field in the
+`securityContext` of Pods or containers to [control use of seccomp
+profiles](/docs/tutorials/clusters/seccomp). In prior versions, seccomp was
+controlled by adding annotations to a Pod. The same PodSecurityPolicies can be
+used with either version to enforce how these fields or annotations are applied.
 
 **seccomp.security.alpha.kubernetes.io/defaultProfileName** - Annotation that
 specifies the default seccomp profile to apply to containers. Possible values
@@ -609,11 +613,18 @@ are:
 - `unconfined` - Seccomp is not applied to the container processes (this is the
   default in Kubernetes), if no alternative is provided.
 - `runtime/default` - The default container runtime profile is used.
-- `docker/default` - The Docker default seccomp profile is used. Deprecated as of
-  Kubernetes 1.11. Use `runtime/default` instead.
+- `docker/default` - The Docker default seccomp profile is used. Deprecated as
+  of Kubernetes 1.11. Use `runtime/default` instead.
 - `localhost/<path>` - Specify a profile as a file on the node located at
   `<seccomp_root>/<path>`, where `<seccomp_root>` is defined via the
-  `--seccomp-profile-root` flag on the Kubelet.
+  `--seccomp-profile-root` flag on the Kubelet. If the `--seccomp-profile-root`
+  flag is not defined, the default path will be used, which is
+  `<root-dir>/seccomp` where `<root-dir>` is specified by the `--root-dir` flag.
+
+{{< note >}}
+  The `--seccomp-profile-root` flag is deprecated since Kubernetes
+  v1.19. Users are encouraged to use the default path.
+{{< /note >}}
 
 **seccomp.security.alpha.kubernetes.io/allowedProfileNames** - Annotation that
 specifies which values are allowed for the pod seccomp annotations. Specified as
@@ -629,15 +640,12 @@ By default, all safe sysctls are allowed.
 - `allowedUnsafeSysctls` - allows specific sysctls that had been disallowed by the default list, so long as these are not listed in `forbiddenSysctls`.
 
 Refer to the [Sysctl documentation](
-/docs/concepts/cluster-administration/sysctl-cluster/#podsecuritypolicy).
-
-
+/docs/tasks/administer-cluster/sysctl-cluster/#podsecuritypolicy).
 
 ## {{% heading "whatsnext" %}}
 
+- See [Pod Security Standards](/docs/concepts/security/pod-security-standards/) for policy recommendations.
 
-See [Pod Security Standards](/docs/concepts/security/pod-security-standards/) for policy recommendations.
-
-Refer to [Pod Security Policy Reference](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podsecuritypolicy-v1beta1-policy) for the api details.
+- Refer to [Pod Security Policy Reference](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podsecuritypolicy-v1beta1-policy) for the api details.
 
 


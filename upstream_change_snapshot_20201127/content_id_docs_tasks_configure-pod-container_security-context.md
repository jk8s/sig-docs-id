diff --git a/content/en/docs/tasks/configure-pod-container/security-context.md b/content/en/docs/tasks/configure-pod-container/security-context.md
index db9a0aa96..10afee864 100644
--- a/content/en/docs/tasks/configure-pod-container/security-context.md
+++ b/content/en/docs/tasks/configure-pod-container/security-context.md
@@ -243,7 +243,7 @@ exit
 
 ## Set capabilities for a Container
 
-With [Linux capabilities](http://man7.org/linux/man-pages/man7/capabilities.7.html),
+With [Linux capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html),
 you can grant certain privileges to a process without granting all the privileges
 of the root user. To add or remove Linux capabilities for a Container, include the
 `capabilities` field in the `securityContext` section of the Container manifest.
@@ -359,6 +359,40 @@ for definitions of the capability constants.
 Linux capability constants have the form `CAP_XXX`. But when you list capabilities in your Container manifest, you must omit the `CAP_` portion of the constant. For example, to add `CAP_SYS_TIME`, include `SYS_TIME` in your list of capabilities.
 {{< /note >}}
 
+## Set the Seccomp Profile for a Container
+
+To set the Seccomp profile for a Container, include the `seccompProfile` field
+in the `securityContext` section of your Pod or Container manifest. The
+`seccompProfile` field is a
+[SeccompProfile](/docs/reference/generated/kubernetes-api/{{< param "version"
+>}}/#seccompprofile-v1-core) object consisting of `type` and `localhostProfile`.
+Valid options for `type` include `RuntimeDefault`, `Unconfined`, and
+`Localhost`. `localhostProfile` must only be set set if `type: Localhost`. It
+indicates the path of the pre-configured profile on the node, relative to the
+kubelet's configured Seccomp profile location (configured with the `--root-dir`
+flag).
+
+Here is an example that sets the Seccomp profile to the node's container runtime
+default profile:
+
+```yaml
+...
+securityContext:
+  seccompProfile:
+    type: RuntimeDefault
+```
+
+Here is an example that sets the Seccomp profile to a pre-configured file at
+`<kubelet-root-dir>/seccomp/my-profiles/profile-allow.json`:
+
+```yaml
+...
+securityContext:
+  seccompProfile:
+    type: Localhost
+    localhostProfile: my-profiles/profile-allow.json
+```
+
 ## Assign SELinux labels to a Container
 
 To assign SELinux labels to a Container, include the `seLinuxOptions` field in


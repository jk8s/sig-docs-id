diff --git a/content/en/docs/home/_index.md b/content/en/docs/home/_index.md
index dcaf69303..68f4bfd3c 100644
--- a/content/en/docs/home/_index.md
+++ b/content/en/docs/home/_index.md
@@ -15,7 +15,7 @@ menu:
     title: "Documentation"
     weight: 20
     post: >
-      <p>Learn how to use Kubernetes with conceptual, tutorial, and reference documentation. You can even <a href="/editdocs/" data-auto-burger-exclude>help contribute to the docs</a>!</p>
+      <p>Learn how to use Kubernetes with conceptual, tutorial, and reference documentation. You can even <a href="/editdocs/" data-auto-burger-exclude data-proofer-ignore>help contribute to the docs</a>!</p>
 description: >
   Kubernetes is an open source container orchestration engine for automating deployment, scaling, and management of containerized applications. The open source project is hosted by the Cloud Native Computing Foundation.
 overview: >
@@ -32,13 +32,13 @@ cards:
   button: "View Tutorials"
   button_path: "/docs/tutorials"
 - name: setup
-  title: "Set up a cluster"
+  title: "Set up a K8s cluster"
   description: "Get Kubernetes running based on your resources and needs."
   button: "Set up Kubernetes"
   button_path: "/docs/setup"
 - name: tasks
   title: "Learn how to use Kubernetes"
-  description: "Look up common tasks and how to perform them using a short sequence of steps."  
+  description: "Look up common tasks and how to perform them using a short sequence of steps."
   button: "View Tasks"
   button_path: "/docs/tasks"
 - name: training
@@ -53,12 +53,14 @@ cards:
   button_path: /docs/reference
 - name: contribute
   title: Contribute to the docs
-  description: Anyone can contribute, whether you’re new to the project or you’ve been around a long time.
+  description: Anyone can contribute, whether you're new to the project or you've been around a long time.
   button: Contribute to the docs
   button_path: /docs/contribute
-- name: download
-  title: Download Kubernetes
+- name: release-notes
+  title: K8s Release Notes
   description: If you are installing Kubernetes or upgrading to the newest version, refer to the current release notes.
+  button: "Download Kubernetes"
+  button_path: "/docs/setup/release/notes"
 - name: about
   title: About the documentation
   description: This website contains documentation for the current and previous 4 versions of Kubernetes.


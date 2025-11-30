// ✅ Bulletproof page-based background control using URL

document.addEventListener("DOMContentLoaded", function () {
  const path = window.location.pathname;

  // ✅ Jobs page
  if (path === "/jobs/" || path.endsWith("/jobs/")) {
    document.querySelector(".md-content").style.background =
  'url("../images/jobs-bg.png") no-repeat center center fixed';
document.querySelector(".md-content").style.backgroundSize = "cover";

  }

  // ✅ Later you can add:
  // if (path === "/grants/" || path.endsWith("/grants/")) { ... }
});

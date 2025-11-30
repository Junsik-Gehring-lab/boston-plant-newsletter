// ✅ Full-page background for Jobs page (edge-to-edge)

document.addEventListener("DOMContentLoaded", function () {
  const path = window.location.pathname;

  // ✅ Detect Jobs page robustly
  if (path === "/jobs/" || path.endsWith("/jobs/")) {

    // ✅ Apply background to the WHOLE PAGE
    document.body.style.background =
      'url("/images/jobs-bg.png") no-repeat center center fixed';
    document.body.style.backgroundSize = "cover";

    // ✅ Remove Material’s white background layers that sit on top
    const layers = document.querySelectorAll(
      ".md-main, .md-main__inner, .md-content"
    );

    layers.forEach(el => {
      el.style.background = "transparent";
    });
  }
});

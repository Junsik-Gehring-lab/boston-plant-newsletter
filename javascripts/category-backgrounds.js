// ✅ Bulletproof full-page background for Jobs page
document.addEventListener("DOMContentLoaded", function () {
  const path = window.location.pathname;

  // ✅ Robust Jobs page detection (works with subpaths)
  if (path.includes("/jobs")) {

    const imgUrl = window.location.origin + "/boston-plant-newsletter/images/jobs-bg.png";

    // ✅ Apply background to full page
    document.body.style.background =
      `url("${imgUrl}") no-repeat center center fixed`;
    document.body.style.backgroundSize = "cover";

    // ✅ Remove Material’s white background layers
    const layers = document.querySelectorAll(
      ".md-main, .md-main__inner, .md-content"
    );

    layers.forEach(el => {
      el.style.background = "transparent";
    });
  }
});

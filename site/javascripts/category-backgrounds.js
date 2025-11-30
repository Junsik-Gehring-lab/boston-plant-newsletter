// ✅ Universal full-page background controller for ALL pages
document.addEventListener("DOMContentLoaded", function () {
  const path = window.location.pathname;

  // ✅ Detect your GitHub Pages project root dynamically
  const projectRoot = "/boston-plant-newsletter";
  const base = window.location.origin + projectRoot;

  // ✅ Map URL → background image
  const bgMap = {
    "/": "home-bg.png",
    "/index.html": "home-bg.png",

    "/jobs": "jobs-bg.png",
    "/grants": "grants-bg.png",
    "/seminars": "seminars-bg.png",
    "/organizations": "organizations-bg.png",
    "/tags": "tags-bg.png",
    "/subscribe": "subscribe-bg.png"
  };

  // ✅ Find which background to use
  let selectedBg = null;

  for (const key in bgMap) {
    if (path === projectRoot + key || path.startsWith(projectRoot + key + "/")) {
      selectedBg = bgMap[key];
      break;
    }
  }

  // ✅ Apply background if matched
  if (selectedBg) {
    const imgUrl = `${base}/images/${selectedBg}`;

    // ✅ Apply full-page background
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

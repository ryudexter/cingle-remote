// Cingle Remote's website: the video's pause button, and a text badge if Apple's badge image doesn't load.
(() => {
  const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  document.querySelectorAll(".film").forEach((film) => {
    const video = film.querySelector("video");
    const button = film.querySelector(".film-toggle");
    if (!video || !button) return;
    const sync = () => {
      const paused = video.paused;
      button.dataset.state = paused ? "paused" : "playing";
      button.setAttribute("aria-label", paused ? button.dataset.play : button.dataset.pause);
    };
    if (still) {
      video.removeAttribute("autoplay");
      video.pause();
    }
    button.addEventListener("click", () => (video.paused ? video.play() : video.pause()));
    video.addEventListener("play", sync);
    video.addEventListener("pause", sync);
    sync();
  });

  document.querySelectorAll(".badge img").forEach((img) => {
    const fallback = () => {
      const text = document.createElement("span");
      text.className = "badge-text";
      text.textContent = img.alt;
      img.replaceWith(text);
    };
    if (img.complete && img.naturalWidth === 0) fallback();
    else img.addEventListener("error", fallback);
  });
})();

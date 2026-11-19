# Cingle Remote's website

GitHub Pages serves `docs/` from `main` at <https://ryudexter.github.io/cingle-remote/>. The repository's root (this support page's `README.md`, `privacy/` and `terms/`) isn't part of the site, so those github.com links stay exactly as the App Store listing has them.

- `site/build.py` holds every page's text and writes the HTML into `docs/`. After changing it, run `python3 site/build.py` from the repository's root and commit `docs/` with it.
- Plain HTML and CSS, no Jekyll (`docs/.nojekyll`). `docs/assets/style.css` and `site.js` are edited by hand.
- Pages: the home page in English (`/`) and Turkish (`/tr/`), one English page per brand (`/lg-tv-remote/`, `/samsung-tv-remote/`, …), and the Turkish Vestel page (`/tr/vestel-kumanda/`). The brand list and what each brand page says follow the support page and the App Store description; keep them in step when TVs are added or dropped.
- App Store links have no country, so Apple opens the visitor's own storefront. The LG, Samsung, Roku, Google TV, Fire TV and Vestel pages link to their brand custom product page (`?ppid=`); the others to the default page. The badge is Apple's own, loaded from Apple's marketing tools.
- No price words (free, trial, discount…) anywhere on the site, as on the store's screenshots. The footer says Cingle isn't affiliated with the TV brands, and carries Apple's trademark line.

## Media

Made from the app repository's `build/store/final/` (gitignored there):

- `assets/video/cingle-<en|tr>.mp4`: the Type on TV opener's 16:9 social cut (`social/Cingle-16x9-1080p-<lang>.mp4`, 28.2 s), without its silent audio:
  `ffmpeg -i <in> -an -vf "scale=1600:-2:flags=lanczos,fps=30" -c:v libx264 -preset slower -crf 23 -profile:v high -pix_fmt yuv420p -movflags +faststart <out>`
- `assets/video/poster-<lang>.jpg`: its frame at 27.2 s ("One remote. All your devices."), 1600 wide. `assets/og-<lang>.jpg`: the same frame at 1200×630, for link previews.
- `assets/shots/*.webp`: store screenshots at 600 wide (`cwebp -q 80 -resize 600 0`). `<brand>-<lang>-*` from `screenshots/cpp/<brand>/<lang>/`, `en-*` from `screenshots/redo/iphone/`, `tr-*` from `screenshots/tr/iphone/`. None of the shots with price words (`*-no-ads`, `mac-too`, `05-mac`) are used.
- Icons from the app's `AppIcon.appiconset`: `icon-128.png` and `favicon-64.png` from `mac-1024.png` (rounded), `apple-touch-icon.png` and `icon-512.png` from `AppIcon.png`.

## Checking it locally

Serve the folder under the same path Pages uses, so the 404 page's links work too:

```bash
mkdir -p /tmp/cingle-site && ln -sfn "$PWD/docs" /tmp/cingle-site/cingle-remote && python3 -m http.server 8765 -d /tmp/cingle-site
```

Then open <http://localhost:8765/cingle-remote/>.

# Canyon Runner — Halloween

Retro pixel endless runner in a spooky vibe. Two builds:

- `web/` — iPhone‑friendly **PWA** (offline support, sound toggle, optional haptics)
- `pygame/` — Desktop **Pygame** “Halloween Edition++”

## Play on the web (GitHub Pages)

This repo is preconfigured to deploy **web/** via GitHub Pages using Actions.

### Quick publish
1. Create a new repo on GitHub (public is fine).
2. On your machine:
   ```bash
   git init
   git add .
   git commit -m "Initial"
   git branch -M main
   git remote add origin https://github.com/<YOUR-USER>/<YOUR-REPO>.git
   git push -u origin main
   ```
3. In GitHub → **Settings → Pages**, set “Build and deployment” to **GitHub Actions**. The included workflow will publish automatically.  
   Your site will appear at `https://<YOUR-USER>.github.io/<YOUR-REPO>/`

> Tip: On iPhone, open the URL in Safari, tap **Share → Add to Home Screen** for full‑screen play. The PWA also works offline after first load.

## Local dev for the web build

Use any static server from the `web/` directory (for service worker + PWA to work):

```bash
cd web
python -m http.server 8080
# open http://localhost:8080
```

## Pygame build (desktop)

```bash
cd pygame
pip install -r requirements.txt
python main.py
```

## License
MIT

# A Little Apology ❤️💀 — Streamlit app

A mobile-first apology experience with four free-text questions, a Rake jumpscare, and an animated letter reveal with falling hearts and optional music.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Run:
   ```bash
   streamlit run app.py
   ```

## Add your media

Create/use the `assets/` folder:

- `assets/the_rake.jpg` — your chosen Rake image (PNG is also supported if named `the_rake.png`)
- `assets/scare.mp3` — a short creepy sound effect (optional)
- `assets/song.mp3` — the song you want during the letter (optional)

Use media you have permission to use. The app does not include copyrighted music or a Rake image, so you can choose the exact versions you want.

## Deploy on Streamlit Community Cloud

1. Put `app.py`, `requirements.txt`, `README.md`, and your `assets/` files in a GitHub repository.
2. Create a new app in Streamlit Community Cloud and select `app.py`.
3. Deploy.

## Mobile notes

- The layout is single-column and designed for narrow screens.
- Browsers may block autoplay audio. The app tries to start audio and provides a play button as a fallback.
- The scare sound is optional and starts only when available. Keep audio at a comfortable volume.
- Answers live in Streamlit session state during the current session; this app does not save them to a database. Do not treat session state as permanent storage.
- The letter can be pasted into the “Add or edit your letter text” expander on the letter screen.

## Customize

- Edit the four question strings in `app.py`.
- Change colors in the CSS near the top of `app.py`.
- Replace the welcome and recovery messages directly in the HTML strings.

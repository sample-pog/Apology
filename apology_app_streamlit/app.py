import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="A Little Apology ❤️",
    page_icon="💗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

ASSET_DIR = Path(__file__).parent / "assets"
RAKE_PATH = ASSET_DIR / "the_rake.jpg"
SONG_PATH = ASSET_DIR / "song.mp3"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
:root { --rose:#b85f75; --ink:#49383c; --cream:#fff8f4; }
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #fff8f4 0%, #fff0f2 100%);
    color: var(--ink);
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stMainBlockContainer"] {
    max-width: 680px;
    padding: 1.15rem 1rem 3rem 1rem;
}
h1, h2, h3 { font-family: 'Playfair Display', Georgia, serif !important; color: #704651; }
p, label, .stMarkdown { color: var(--ink); }
div.stButton > button {
    width: 100%; min-height: 3.15rem; border-radius: 16px;
    border: 1px solid #e6b9c4; background: #b85f75; color: white;
    font-size: 1rem; font-weight: 700; padding: .7rem 1rem;
    transition: transform .15s ease, background .15s ease;
}
div.stButton > button:hover { background: #a64d64; border-color: #a64d64; color:white; transform: translateY(-1px); }
div.stButton > button:focus { box-shadow: 0 0 0 .2rem #f3c8d2; }
.stTextArea textarea {
    border-radius: 14px !important; border: 1px solid #e5c7ce !important;
    background: rgba(255,255,255,.88) !important; font-size: 1rem !important;
    line-height: 1.55 !important;
}
div[data-testid="stProgress"] > div > div { background-color: #b85f75; }
.small-note { color:#9a737b; font-size:.88rem; text-align:center; }
.hero {
    padding: 1.5rem 1.15rem; border:1px solid #f0d6dc; border-radius:24px;
    background:rgba(255,255,255,.67); text-align:center; box-shadow:0 8px 28px #8f52600c;
}
.eyebrow { color:#b85f75; letter-spacing:.12em; text-transform:uppercase; font-size:.72rem; font-weight:700; }
.letter-card {
    background:#fffdf9; border:1px solid #ead8ce; border-radius:8px 8px 22px 22px;
    padding:1.4rem 1.1rem; box-shadow:0 12px 30px #76465012; white-space:pre-wrap;
    line-height:1.8; font-size:1rem; overflow-wrap:anywhere;
}
.rake-warning { text-align:center; font-size:.82rem; color:#8e777c; }
@media (max-width: 480px) {
  [data-testid="stMainBlockContainer"] { padding: .75rem .75rem 2rem .75rem; }
  h1 { font-size: 2rem !important; }
  h2 { font-size: 1.55rem !important; }
  .hero { padding: 1.2rem .9rem; border-radius:20px; }
}
</style>
""", unsafe_allow_html=True)

def file_data_uri(path, mime):
    if not path.exists():
        return None
    raw = path.read_bytes()
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"

if "stage" not in st.session_state:
    st.session_state.stage = "welcome"
if "answers" not in st.session_state:
    st.session_state.answers = ["", "", "", ""]
if "jump_seen" not in st.session_state:
    st.session_state.jump_seen = False

questions = [
    "How are you feeling right now?",
    "What hurt the most?",
    "What do you need from me right now?",
    "Can we try to fix this together?",
]

def move(stage):
    st.session_state.stage = stage

def go_back(target):
    st.session_state.stage = target

# WELCOME
if st.session_state.stage == "welcome":
    st.markdown("""
    <div class="hero">
      <div style="font-size:2.7rem;margin-bottom:.3rem">💗</div>
      <div class="eyebrow">A little something for you</div>
      <h1 style="margin:.5rem 0 .7rem">Hey, my love.</h1>
      <p style="font-size:1.05rem;line-height:1.7;margin-bottom:.4rem">
      I made this little page because I want to listen to you, understand you,
      and tell you something that matters to me.
      </p>
      <div style="font-size:1.25rem;margin-top:.7rem">♡</div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Let's begin ❤️", key="begin"):
        move("questions")
        st.rerun()
    st.markdown('<p class="small-note">Made with love, one little step at a time.</p>', unsafe_allow_html=True)

# QUESTIONS
elif st.session_state.stage == "questions":
    idx = st.session_state.get("question_index", 0)
    idx = max(0, min(3, idx))
    st.session_state.question_index = idx
    st.progress((idx + 1) / 4, text=f"Question {idx + 1} of 4")
    st.markdown(f'<div class="eyebrow">A moment to listen</div><h1 style="margin-top:.4rem">{questions[idx]}</h1>', unsafe_allow_html=True)
    st.caption("Write whatever you want to say. There are no right or wrong answers.")
    answer = st.text_area(
        "Your answer",
        value=st.session_state.answers[idx],
        key=f"answer_{idx}",
        height=155,
        placeholder="I'm listening…",
        label_visibility="collapsed",
    )
    st.session_state.answers[idx] = answer
    c1, c2 = st.columns(2, gap="small")
    with c1:
        if idx > 0 and st.button("← Back", key="qback"):
            st.session_state.answers[idx] = answer
            st.session_state.question_index = idx - 1
            st.rerun()
    with c2:
        label = "Continue →" if idx < 3 else "Continue to the letter…"
        if st.button(label, key="qnext"):
            st.session_state.answers[idx] = answer
            if idx < 3:
                st.session_state.question_index = idx + 1
                st.rerun()
            else:
                move("setup")
                st.rerun()
    st.markdown('<p class="small-note">You can leave a question blank if you want.</p>', unsafe_allow_html=True)

# PRE-PRANK SETUP
elif st.session_state.stage == "setup":
    st.markdown("""
    <div class="hero">
      <div style="font-size:2.2rem">💌</div>
      <h1>Okay, one last thing…</h1>
      <p style="line-height:1.7">I made something for you. Tap below to open it.</p>
      <p class="small-note">Just a tiny warning: this next bit contains a sudden horror image and sound.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Open this letter 💌", key="fake_letter"):
        move("jumpscare")
        st.rerun()
    st.markdown('<p class="rake-warning">Sound is optional. Please keep your volume comfortable.</p>', unsafe_allow_html=True)

# JUMPSCARE
elif st.session_state.stage == "jumpscare":
    rake_uri = file_data_uri(RAKE_PATH, "image/jpeg")
    if not rake_uri:
        rake_uri = file_data_uri(RAKE_PATH.with_suffix(".png"), "image/png")
    if rake_uri:
        image_markup = f'<img class="rake" src="{rake_uri}" alt="The Rake creepypasta creature">'
    else:
        image_markup = """
        <div class="placeholder-rake" role="img" aria-label="The Rake image is not installed">
          <div class="eyes">●　　　●</div><div class="mouth">╱╲╱╲</div>
          <div class="missing">Add assets/the_rake.jpg to use your Rake image.</div>
        </div>
        """
    sound_uri = file_data_uri(ASSET_DIR / "scare.mp3", "audio/mpeg")
    audio_markup = f'<audio id="scareAudio" src="{sound_uri}" preload="auto"></audio>' if sound_uri else ""
    components.html(f"""
    <style>
      * {{ box-sizing:border-box; }}
      html,body {{ margin:0;background:#050407;color:#fff;font-family:system-ui,sans-serif; }}
      .scene {{ position:relative; min-height:76vh; display:flex; flex-direction:column; align-items:center; justify-content:center; overflow:hidden; padding:1rem .6rem; background:radial-gradient(ellipse at center,#321b24 0%,#100d13 48%,#030304 100%); animation:flash .28s 1; }}
      .rake {{ width:100%; max-width:580px; max-height:67vh; object-fit:contain; filter:contrast(1.15) saturate(.65); animation:shake .13s 7; }}
      .placeholder-rake {{ width:100%; min-height:55vh; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#f4edf2; background:linear-gradient(145deg,#151016,#050407); }}
      .eyes {{ font-size:clamp(2rem,10vw,5rem); color:#f5e6e8; text-shadow:0 0 20px #ff1d43; }}
      .mouth {{ font-size:clamp(2rem,10vw,5rem); margin-top:1rem; }}
      .missing {{ font-size:.75rem;color:#c8b6bf;text-align:center;margin:2rem; }}
      h1 {{ color:#ff344e;font-size:clamp(2rem,9vw,4rem);line-height:1.02;text-align:center;margin:.5rem 0;text-shadow:0 0 16px #b80028; }}
      p {{ text-align:center;color:#e7dce2; }}
      @keyframes shake {{ 0%,100%{{transform:translate(0,0) scale(1.02)}} 25%{{transform:translate(-5px,3px) scale(1.04)}} 50%{{transform:translate(5px,-2px) scale(1.03)}} 75%{{transform:translate(-3px,-3px) scale(1.05)}} }}
      @keyframes flash {{ 0%{{filter:brightness(5)}} 100%{{filter:brightness(1)}} }}
      @media(prefers-reduced-motion:reduce) {{ .rake,.scene {{ animation:none; }} }}
    </style>
    <div class="scene">
      {image_markup}
      <h1>THE RAKE.</h1>
      <p>YOU THOUGHT IT WAS A LETTER. 💀</p>
      {audio_markup}
      <button id="soundBtn" style="border:1px solid #9e5969;border-radius:12px;background:#24131a;color:white;padding:.7rem 1rem;font-size:1rem">🔊 Play scare sound</button>
    </div>
    <script>
      const audio = document.getElementById('scareAudio');
      const btn = document.getElementById('soundBtn');
      if(audio) {{
        audio.volume = 0.55;
        // Browsers may block autoplay. The button is a reliable tap-to-play fallback.
        audio.play().catch(()=>{{}});
        btn.addEventListener('click',()=>{{ audio.currentTime=0; audio.play().catch(()=>{{}}); }});
      }} else {{
        btn.textContent = '🔇 Add assets/scare.mp3 for the sound';
        btn.disabled = true;
        btn.style.opacity = '.7';
      }}
    </script>
    """, height=590, scrolling=False)
    st.write("")
    st.markdown('<p style="text-align:center;font-size:1rem">OKAY OKAY, I’M SORRY 😭</p>', unsafe_allow_html=True)
    if st.button("I'M SORRY 😭 Show me the real letter", key="recover"):
        move("recovery")
        st.rerun()

# RECOVERY
elif st.session_state.stage == "recovery":
    st.markdown("""
    <div class="hero">
      <div style="font-size:2.7rem">😭💗</div>
      <h1>OKAY, I'M SORRY.</h1>
      <p style="line-height:1.7">That was absolutely not the letter I meant. I had to be a little menace first.</p>
      <p style="line-height:1.7">Here's the real one. I mean this part with all my heart.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Open the REAL letter 💌", key="real_letter"):
        move("letter")
        st.rerun()

# REAL LETTER
elif st.session_state.stage == "letter":
    st.markdown('<div class="eyebrow" style="text-align:center">For you, always</div><h1 style="text-align:center">A letter for my love 💗</h1>', unsafe_allow_html=True)
    # User writes their letter in this file or via the app's optional text box.
    if "letter_text" not in st.session_state:
        st.session_state.letter_text = ""
    with st.expander("Add or edit your letter text", expanded=not bool(st.session_state.letter_text)):
        st.session_state.letter_text = st.text_area(
            "Your letter",
            value=st.session_state.letter_text,
            height=220,
            placeholder="Paste the letter you've written here…",
            key="letter_editor",
            help="This stays in the current app session; it is not saved to a database.",
        )
    music_uri = file_data_uri(SONG_PATH, "audio/mpeg")
    if music_uri:
        music_html = f"""
        <audio id="loveSong" src="{music_uri}" preload="auto" loop></audio>
        <button id="musicBtn" style="border:1px solid #e6b9c4;border-radius:999px;background:#fff1f4;color:#8b4559;padding:.7rem 1rem;font-size:1rem;font-weight:600">♫ Play the song</button>
        <script>
          const song=document.getElementById('loveSong');
          const mb=document.getElementById('musicBtn');
          song.volume=0.32;
          // Try to start on page load; if blocked, the visible button lets the user start it.
          song.play().then(()=>{{mb.textContent='♫ Pause the song';}}).catch(()=>{{}});
          mb.addEventListener('click',()=>{{
            if(song.paused){{song.play().then(()=>mb.textContent='♫ Pause the song').catch(()=>{{}});}}
            else{{song.pause();mb.textContent='♫ Play the song';}}
          }});
        </script>
        """
    else:
        music_html = """
        <button disabled style="border:1px solid #e6b9c4;border-radius:999px;background:#fff1f4;color:#8b4559;padding:.7rem 1rem;font-size:1rem">♫ Add assets/song.mp3 to play your song</button>
        """
    # Heart shower and letter opening effect
    letter_text = st.session_state.letter_text.strip()
    safe_letter = (letter_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")) if letter_text else "Your letter will appear here once you add your words above. 💗"
    components.html(f"""
    <style>
      *{{box-sizing:border-box}}
      body{{margin:0;background:transparent;font-family:Georgia,serif;color:#5b3c45}}
      .wrap{{position:relative;overflow:hidden;padding:.35rem 0 1rem}}
      .music{{text-align:center;margin:.2rem 0 1rem}}
      .envelope{{margin:0 auto 1rem;width:min(220px,70vw);height:145px;position:relative;background:#f7dfe4;border:1px solid #e6b9c4;border-radius:8px;box-shadow:0 10px 25px #74404b18;display:flex;align-items:center;justify-content:center;}}
      .envelope:before{{content:"";position:absolute;top:0;left:0;width:0;height:0;border-left:calc(min(220px,70vw) / 2) solid transparent;border-right:calc(min(220px,70vw) / 2) solid transparent;border-top:78px solid #efc7d0;transform-origin:top;animation:openFlap 1.1s .25s forwards;z-index:2}}
      .seal{{position:relative;z-index:3;font-size:2rem;animation:sealAway .45s .35s forwards}}
      .letter{{position:relative;background:#fffdf9;border:1px solid #ead8ce;border-radius:10px;padding:1.25rem 1rem;line-height:1.85;font-size:1rem;white-space:pre-wrap;overflow-wrap:anywhere;box-shadow:0 12px 30px #76465012;opacity:0;transform:translateY(24px) scale(.98);animation:letterRise 1s 1s forwards;min-height:120px}}
      .hearts{{position:absolute;inset:0;pointer-events:none;overflow:hidden;z-index:5}}
      .heart{{position:absolute;top:-35px;font-size:clamp(16px,5vw,27px);animation:fall linear forwards;filter:drop-shadow(0 2px 2px #b85f7520)}}
      @keyframes openFlap{{to{{transform:rotateX(180deg);filter:brightness(.96)}}}}
      @keyframes sealAway{{to{{opacity:0;transform:scale(.5)}}}}
      @keyframes letterRise{{to{{opacity:1;transform:translateY(0) scale(1)}}}}
      @keyframes fall{{to{{transform:translate3d(var(--drift),110vh,0) rotate(540deg);opacity:.15}}}}
      @media(prefers-reduced-motion:reduce){{.envelope:before,.seal,.letter,.heart{{animation:none!important}}.letter{{opacity:1;transform:none}}}}
    </style>
    <div class="wrap">
      <div class="music">{music_html}</div>
      <div class="envelope"><div class="seal">💗</div></div>
      <div class="hearts" id="hearts"></div>
      <div class="letter">{safe_letter}</div>
    </div>
    <script>
      const holder=document.getElementById('hearts');
      const symbols=['♥','♡','💗','💕','❤'];
      for(let i=0;i<34;i++){{
        const h=document.createElement('span'); h.className='heart';
        h.textContent=symbols[Math.floor(Math.random()*symbols.length)];
        h.style.left=(Math.random()*100)+'%';
        h.style.animationDelay=(Math.random()*1.5)+'s';
        h.style.animationDuration=(3.5+Math.random()*3)+'s';
        h.style.setProperty('--drift',((Math.random()-.5)*120)+'px');
        h.style.color=['#d77c94','#ef9eb2','#c45d79','#f3b6c6'][i%4];
        holder.appendChild(h);
      }}
    </script>
    """, height=660, scrolling=False)
    st.markdown('<p class="small-note">If the song does not start automatically, tap “Play the song”. Mobile browsers sometimes require a direct tap before audio can play.</p>', unsafe_allow_html=True)
    if st.button("Back to the beginning ↺", key="restart"):
        for key in ["question_index", "letter_text", "letter_editor"]:
            st.session_state.pop(key, None)
        st.session_state.answers = ["", "", "", ""]
        move("welcome")
        st.rerun()

st.markdown('<p class="small-note" style="margin-top:2rem">Made with love (and questionable decisions) ❤️</p>', unsafe_allow_html=True)

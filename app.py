"""
The Run
A birthday gift, played act by act.

Layout of this file
  1. Config and content      (edit names, story text, photos, quests here)
  2. Styles                  (all custom CSS)
  3. State and navigation    (session state, gating)
  4. Helpers                 (small HTML builders)
  5. Screens                 (intro, act 1, act 2, vault, act 3, victory)
  6. Router

Photos: drop image files into the "photos" folder next to this file, named to
match each node's "photo" field (01_match_found.jpg, 02_first_contact.png, ...).
The extension can be jpg, jpeg, png, webp or gif, and capitals do not matter.
Any node whose photo is missing shows the dashed placeholder box.
"""

import base64
import html as html_lib
import mimetypes
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


# =============================================================================
# 1. CONFIG AND CONTENT
# =============================================================================

HIS_NAME = "binhbun"
HER_NAME = "monbon"
RUN_STARTED = "6 December 2025"
PHOTO_DIR = Path(__file__).parent / "photos"

ACT1_NODES = [
    {
        "tag": "New Save File Started",
        "date": "16 September",
        "title": "Match Found",
        "photo": "01_match_found",
        "body": (
            "Our very first message on Coffee Meets Bagel. You opened with a story "
            "about rollerblading, and how you could not do it at all, then asked if "
            "I could teach you sometime. I am pretty sure you don't wanna do "
            "that anymore."
        ),
        "acquired": "Trait acquired: Secretly Uncoordinated",
    },
    {
        "tag": "Tutorial Level",
        "date": "11 October",
        "title": "First Contact",
        "photo": "02_first_contact",
        "body": (
            "It took until October for us to actually meet. Gami chicken in Werribee. "
            "We talked for hours about nothing and everything. Looking back, making "
            "you wait that long feels a little silly now."
        ),
        "acquired": "Relic acquired: The Long Wait",
    },
    {
        "tag": "First Spark",
        "date": "8 November",
        "title": "Yarra Lights",
        "photo": "03_yarra_lights",
        "body": (
            "A quiet, drizzly night. Walking along the Yarra with the city lights "
            "across the water. Somewhere along that bridge, our hands found each "
            "other for the first time."
        ),
        "acquired": "Relic acquired: First Spark",
    },
    {
        "tag": "Tension Rising",
        "date": "23 November",
        "title": "The Rock",
        "photo": "04_the_rock",
        "body": (
            "Sitting by the rock near the lake by my house. The tension was about as "
            "high as it gets. The night ended with a shy little peck. Unofficial, but "
            "very much felt."
        ),
        "acquired": "Achievement unlocked: Braved The Rock",
    },
    {
        "tag": "Act 1 Boss Clear",
        "date": "6 December",
        "title": "Point Lonsdale",
        "photo": "05_point_lonsdale",
        "body": (
            "A windy beach day in Point Lonsdale and Queenscliff. You asked me to be "
            "yours in the sweetest way possible. I said yes. Officially girlfriend "
            "and boyfriend from this day."
        ),
        "acquired": "New status unlocked: Together",
    },
]

ACT2_NODES = [
    {
        "title": "Alt Pasta Bar",
        "photo": "06_alt_pasta_bar",
        "body": (
            "The first fancy outing. You served everything onto my plate before "
            "touching your own. I noticed. And I love it."
        ),
        "acquired": "Relic acquired: The Gentleman's Serve",
    },
    {
        "title": "Mr Lee's, CBD",
        "photo": "07_mr_lees",
        "body": (
            "Sundae, pork blood, and innards, and somehow still one of the best "
            "Korean spots in town. You told me eating there reminds you how grateful "
            "you are to have someone who would try something like this with you."
            " I'll never forget that."
        ),
        "acquired": "Relic acquired: Not Everyone Eats Sundae With You",
    },
    {
        "title": "Nomad",
        "photo": "08_nomad",
        "body": (
            "5 out of 5. No notes. You took me here for my birthday and it was one "
            "of the best experiences we have had together. Are you excited to find out where I'm taking you?"
        ),
        "acquired": "Relic acquired: A Perfect Score",
    },
    {
        "title": "The Kitchen Duo",
        "photo": "09_kitchen_duo",
        "body": (
            "So many staycation cooking sessions, but the seafood boil and the beef "
            "wellington were elite. Don't get me started on the taco night that we hosted!"
            " Honestly, what CAN'T we do at "
            "this point."
        ),
        "acquired": "Relic acquired: Certified Pros",
    },
    {
        "title": "Sunset Hour",
        "photo": "10_sunset_hour",
        "body": (
            "Sephora, trying Goldfield and Banks Sunset Hour. We both loved it so "
            "much you wanted to buy it for the two of us to share once we move in "
            "together. I just love how much we talk about our house in the future."
        ),
        "acquired": "Relic acquired: Scented Future",
    },
    {
        "title": "Kyneton",
        "photo": "11_kyneton",
        "body": (
            "Infinite fun. 😉 Kyneton knows what happened. You know too. Some relics do not need an "
            "explanation."
        ),
        "acquired": "Relic acquired: Kyneton, details classified",
    },
]

# answer = None means any non empty answer opens the lock
VAULT_LOCKS = [
    {"question": "What do we always say before we eat?", "answer": "cheers"},
    {"question": "What was the first movie we watched together?", "answer": "now you see me"},
    {"question": "Are you enjoying your gift?", "answer": None},
]

PUSHES_NEEDED = 5
PUSH_LINES = [
    "It is heavy. Give it a push.",
    "It creaks.",
    "Something shifts on the other side.",
    "Light is coming through the gap.",
    "Nearly there. One more.",
]

# Times are Melbourne local. AEDT (UTC+11) is in effect on 24 October.
QUESTS = [
    {
        "key": "scent",
        "number": "Quest 1",
        "title": "The Scent Quest",
        "desc": "A DIY Korean perfume making class for the two of us, private group, at Shizuku.",
        "when": "Saturday 24 October 2026, 2:30pm until 4:30pm",
        "where": "Shizuku Workshop, 923 Collins Street, Docklands",
        "link": "https://www.instagram.com/shizuku.theworkshop/",
        "start_iso": "2026-10-24T14:30:00+11:00",
        "end_iso": "2026-10-24T16:30:00+11:00",
    },
    {
        "key": "feast",
        "number": "Quest 2",
        "title": "The Feast",
        "desc": "Dinner at Langlands. Table for two, and you are not allowed to serve me first this time.",
        "when": "Saturday 24 October 2026, 5:30pm",
        "where": "Langlands Restaurant and Bar, Hyatt Centric Melbourne",
        "link": "https://www.instagram.com/langlandsmelbourne/",
        "start_iso": "2026-10-24T17:30:00+11:00",
        "end_iso": "2026-10-24T20:30:00+11:00",
    },
]


# =============================================================================
# 2. STYLES
# =============================================================================

BRICK_SVG = (
    "data:image/svg+xml;utf8,"
    "<svg xmlns='http://www.w3.org/2000/svg' width='120' height='60'>"
    "<rect width='120' height='60' fill='%23ddd0b6'/>"
    "<rect x='2' y='2' width='56' height='26' fill='%23e3d7bf'/>"
    "<rect x='62' y='2' width='56' height='26' fill='%23d8caae'/>"
    "<rect x='-28' y='32' width='56' height='26' fill='%23d6c7aa'/>"
    "<rect x='32' y='32' width='56' height='26' fill='%23e1d4ba'/>"
    "<rect x='92' y='32' width='56' height='26' fill='%23dbcdb2'/>"
    "</svg>"
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,800;0,9..144,900;1,9..144,400&family=Nunito:wght@400;600;700&display=swap');

:root {
  --cream: #fbf6ec;
  --sand: #f4ede1;
  --sand-deep: #ece1cd;
  --ink: #4a3b2a;
  --ink-soft: #6b5638;
  --ink-faint: #9a8567;
  --gold: #b98f4e;
  --gold-deep: #9c7538;
  --tan: #e4d2ac;
  --line: #e2d5bd;
  --stamp: #a4553a;
}

/* ---------- page ---------- */
html, body, [data-testid="stAppViewContainer"], .stApp {
  background: var(--sand) !important;
  color: var(--ink);
  font-family: 'Nunito', 'Segoe UI', system-ui, sans-serif;
}
[data-testid="stAppViewContainer"] {
  background:
    radial-gradient(ellipse at top, rgba(255,255,255,0.55), transparent 60%),
    var(--sand) !important;
}
header[data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }
.block-container { max-width: 720px; padding-top: 2.5rem; padding-bottom: 4rem; }
p, li, label, input { font-family: 'Nunito', 'Segoe UI', system-ui, sans-serif; color: var(--ink); }
h1, h2, h3, h4 { font-family: 'Fraunces', Georgia, serif !important; color: var(--ink) !important; }

@keyframes rise { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }

[data-testid="stHeaderActionElements"], h1 a, h2 a, h3 a { display: none !important; }
[class*="st-key-quest-"] [data-testid="stMarkdownContainer"], .st-key-door-wrap [data-testid="stMarkdownContainer"] { margin-bottom: 0 !important; }

[data-testid="stElementContainer"]:has(iframe[height="0"]) { position: absolute; width: 0; height: 0; overflow: hidden; }

/* ---------- run map ---------- */
.run-map {
  display: flex; align-items: center; justify-content: center;
  gap: 0; margin: 0 0 1.8rem 0; flex-wrap: nowrap;
}
.run-map .stop {
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  font-size: 0.68rem; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--ink-faint); font-weight: 700; min-width: 48px;
}
.run-map .pin {
  width: 14px; height: 14px; border-radius: 50%;
  border: 2px solid var(--tan); background: var(--cream);
}
.run-map .stop.done .pin { background: var(--gold); border-color: var(--gold); }
.run-map .stop.done { color: var(--ink-soft); }
.run-map .stop.here .pin {
  background: var(--cream); border-color: var(--gold);
  box-shadow: 0 0 0 4px rgba(185,143,78,0.22);
}
.run-map .stop.here { color: var(--ink); }
.run-map .path { flex: 1; max-width: 70px; height: 2px; margin-bottom: 20px;
  background: repeating-linear-gradient(90deg, var(--tan) 0 5px, transparent 5px 10px); }
.run-map .path.done { background: var(--gold); }

/* ---------- act header ---------- */
.act-head { text-align: center; margin-bottom: 1.2rem; animation: rise .5s ease both; }
.act-head .eyebrow {
  font-size: 0.75rem; letter-spacing: 0.28em; text-transform: uppercase;
  color: var(--gold-deep); font-weight: 700;
}
.act-head h1 {
  font-size: 2.3rem; font-weight: 800; margin: 0.15rem 0 0.2rem; padding: 0;
  letter-spacing: -0.01em;
}
.act-head .sub { color: var(--ink-soft); font-size: 0.98rem; margin: 0; }

/* ---------- progress dots ---------- */
.dots { display: flex; justify-content: center; align-items: center; gap: 10px; margin: 0.4rem 0 0.3rem; }
.dots .dot {
  width: 10px; height: 10px; border-radius: 50%; background: var(--tan); opacity: .55;
  transition: all .3s ease;
}
.dots .dot.done { background: var(--gold); opacity: 1; }
.dots .dot.now { width: 28px; border-radius: 10px; background: var(--gold); opacity: 1; }
.dots-label { text-align: center; font-size: 0.78rem; color: var(--ink-faint); margin-bottom: 1.1rem;
  letter-spacing: 0.06em; }

/* ---------- node card ---------- */
.node-card {
  background: var(--cream); border: 1px solid var(--line); border-radius: 22px;
  padding: 1.7rem 1.7rem 1.4rem; box-shadow: 0 10px 30px -18px rgba(74,59,42,0.35);
  animation: rise .45s ease both;
}
.node-meta { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }
.tag {
  display: inline-block; background: var(--tan); color: var(--ink);
  font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase;
  padding: 5px 11px; border-radius: 999px;
}
.node-date { font-family: 'Fraunces', Georgia, serif; font-style: italic; color: var(--ink-soft); font-size: 0.98rem; }
.node-title { font-family: 'Fraunces', Georgia, serif; font-weight: 800; font-size: 1.9rem;
  color: var(--ink); margin: 0.7rem 0 1rem; line-height: 1.1; }
.photo {
  width: 100%; aspect-ratio: 4 / 3; border-radius: 16px; overflow: hidden;
  background: var(--sand);
}
.photo img { width: 100%; height: 100%; object-fit: cover; display: block; }
.photo.placeholder {
  border: 2px dashed #cdb892; background:
    repeating-linear-gradient(135deg, rgba(228,210,172,0.18) 0 12px, transparent 12px 24px), var(--sand);
  display: flex; align-items: center; justify-content: center;
}
.photo.placeholder span {
  font-size: 0.8rem; letter-spacing: 0.2em; text-transform: uppercase; color: var(--ink-faint); font-weight: 700;
}
.node-body { font-size: 1.05rem; line-height: 1.7; color: var(--ink); margin: 1.2rem 0 1.2rem; }
.acquired {
  display: flex; align-items: center; gap: 12px;
  border-top: 1px dashed var(--tan); padding-top: 1rem;
}
.acquired .gem {
  width: 30px; height: 30px; flex: none; transform: rotate(45deg); border-radius: 6px;
  background: linear-gradient(135deg, #e9d3a3, var(--gold) 60%, var(--gold-deep));
  box-shadow: 0 0 0 3px rgba(185,143,78,0.18), inset 0 1px 0 rgba(255,255,255,.5);
}
.acquired .kind { font-size: 0.7rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--gold-deep); font-weight: 700; }
.acquired .name { font-family: 'Fraunces', Georgia, serif; font-size: 1.1rem; font-weight: 600; color: var(--ink); line-height: 1.2; }

/* ---------- buttons ---------- */
.stButton > button, [data-testid="stFormSubmitButton"] > button {
  font-family: 'Nunito', 'Segoe UI', system-ui, sans-serif; font-weight: 700; letter-spacing: 0.04em;
  border-radius: 999px; padding: 0.62rem 1.5rem; transition: all .2s ease;
  width: 100%;
}
.stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] > button {
  background: var(--gold); color: #fffaf0; border: 1px solid var(--gold-deep);
  box-shadow: 0 6px 16px -8px rgba(156,117,56,0.8);
}
.stButton > button[kind="primary"]:hover, [data-testid="stFormSubmitButton"] > button:hover {
  background: var(--gold-deep); color: #fffaf0; border-color: var(--gold-deep); transform: translateY(-1px);
}
.stButton > button[kind="primary"]:focus:not(:active) { color: #fffaf0; border-color: var(--gold-deep); }
.stButton > button[kind="secondary"] {
  background: transparent; color: var(--ink-soft); border: 1px solid var(--tan);
}
.stButton > button[kind="secondary"]:hover { border-color: var(--gold); color: var(--ink); background: var(--cream); }
.stButton > button p, [data-testid="stFormSubmitButton"] > button p { color: inherit; font-weight: 700; }
.spacer { height: 0.9rem; }

/* ---------- intro ---------- */
.intro { text-align: center; padding: 3rem 0.5rem 1.5rem; animation: rise .7s ease both; }
.intro .crest {
  width: 74px; height: 74px; margin: 0 auto 1.4rem; border-radius: 50%;
  border: 2px solid var(--gold); display: flex; align-items: center; justify-content: center;
  background: var(--cream); box-shadow: 0 0 0 7px rgba(185,143,78,0.12);
}
.intro .crest div { width: 22px; height: 22px; transform: rotate(45deg); border-radius: 4px;
  background: linear-gradient(135deg, #e9d3a3, var(--gold) 60%, var(--gold-deep)); }
.intro .eyebrow { font-size: 0.78rem; letter-spacing: 0.3em; text-transform: uppercase; color: var(--gold-deep); font-weight: 700; }
.intro h1 { font-size: 4.2rem; font-weight: 900; margin: 0.2rem 0 0.6rem; letter-spacing: -0.02em; line-height: 1; }
.intro .lede { font-family: 'Fraunces', Georgia, serif; font-style: italic; font-size: 1.25rem; color: var(--ink-soft); margin-bottom: 1.6rem; }
.intro .copy { max-width: 470px; margin: 0 auto; font-size: 1.05rem; line-height: 1.75; color: var(--ink); }
.intro .rules { margin-top: 1.8rem; font-size: 0.75rem; letter-spacing: 0.22em; text-transform: uppercase; color: var(--ink-faint); font-weight: 700; }

/* ---------- vault ---------- */
.st-key-vault {
  background-image:
    radial-gradient(circle at 8% 4%, rgba(233,190,110,0.55), transparent 32%),
    radial-gradient(circle at 92% 4%, rgba(233,190,110,0.55), transparent 32%),
    radial-gradient(ellipse at 50% 120%, rgba(74,59,42,0.22), transparent 60%),
    url("BRICK_SVG");
  border: 1px solid #c7b392; border-radius: 26px; padding: 1.6rem 1.4rem 1.8rem;
  box-shadow: inset 0 0 60px rgba(74,59,42,0.18), 0 14px 34px -20px rgba(74,59,42,0.55);
  gap: 0.9rem;
}
.vault-head { text-align: center; position: relative; padding: 0.4rem 3.2rem 0.2rem; }
.vault-head .eyebrow { font-size: 0.74rem; letter-spacing: 0.3em; text-transform: uppercase; color: var(--gold-deep); font-weight: 700; }
.vault-head h1 { font-size: 2.5rem; font-weight: 900; margin: 0.1rem 0 0.2rem; padding: 0;
  text-shadow: 0 1px 0 rgba(255,255,255,0.5); }
.vault-head .sub { font-family: 'Fraunces', Georgia, serif; font-style: italic; font-size: 1.2rem; color: var(--ink-soft); margin: 0; }
.vault-head .blurb { font-size: 0.95rem; color: var(--ink-soft); margin: 0.7rem auto 0; max-width: 420px; line-height: 1.6; }
.torch { position: absolute; top: 6px; width: 16px; }
.torch.l { left: 6px; } .torch.r { right: 6px; }
.torch .flame {
  width: 16px; height: 22px; margin: 0 auto;
  background: radial-gradient(ellipse at 50% 80%, #fff3cf 0%, #f2c86b 40%, #d98a32 75%, transparent 76%);
  border-radius: 50% 50% 45% 45% / 65% 65% 35% 35%;
  animation: flicker 1.6s ease-in-out infinite alternate; transform-origin: 50% 100%;
  filter: drop-shadow(0 0 8px rgba(242,200,107,0.9));
}
.torch.r .flame { animation-delay: .5s; }
.torch .stick { width: 6px; height: 34px; margin: 0 auto; border-radius: 2px;
  background: linear-gradient(#7b5a33, #4a3b2a); }
.torch .cup { width: 16px; height: 6px; margin: -38px auto 32px; border-radius: 2px 2px 6px 6px; background: #5a452d; position: relative; }
@keyframes flicker {
  0% { transform: scale(1, 1) rotate(-2deg); opacity: .92; }
  50% { transform: scale(0.92, 1.08) rotate(2deg); opacity: 1; }
  100% { transform: scale(1.05, 0.95) rotate(-1deg); opacity: .88; }
}

[class*="st-key-lock-"] {
  background: rgba(251,246,236,0.9); border: 1px solid #cdb892; border-radius: 18px;
  padding: 1.1rem 1.2rem 1.2rem; gap: 0.5rem;
  box-shadow: 0 8px 20px -14px rgba(74,59,42,0.6);
}
.lock-row { display: flex; align-items: center; gap: 14px; padding-bottom: 0.35rem; }
[class*="st-key-lock-"] [data-testid="stMarkdownContainer"], .st-key-vault [data-testid="stMarkdownContainer"] { margin-bottom: 0 !important; }
.keyhole {
  width: 42px; height: 42px; border-radius: 50%; flex: none; position: relative;
  background: radial-gradient(circle at 35% 30%, #8a7a66, #4a3b2a 70%);
  box-shadow: inset 0 2px 3px rgba(255,255,255,0.25), 0 0 0 3px #d2c19f;
}
.keyhole::before { content: ""; position: absolute; left: 50%; top: 11px; width: 10px; height: 10px;
  margin-left: -5px; border-radius: 50%; background: #1f1810; }
.keyhole::after { content: ""; position: absolute; left: 50%; top: 18px; margin-left: -4px;
  border-left: 4px solid transparent; border-right: 4px solid transparent; border-bottom: 13px solid #1f1810; }
.keyhole.open {
  background: radial-gradient(circle at 35% 30%, #f3dca6, var(--gold) 65%, var(--gold-deep));
  box-shadow: inset 0 2px 3px rgba(255,255,255,0.5), 0 0 0 3px var(--tan), 0 0 18px rgba(233,190,110,0.8);
}
.keyhole.open::before, .keyhole.open::after { opacity: 0.25; }
.lock-text { flex: 1; }
.lock-num { font-size: 0.68rem; letter-spacing: 0.2em; text-transform: uppercase; color: var(--ink-faint); font-weight: 700; }
.lock-q { font-family: 'Fraunces', Georgia, serif; font-size: 1.15rem; font-weight: 600; color: var(--ink); line-height: 1.25; }
.status { font-size: 0.66rem; letter-spacing: 0.16em; text-transform: uppercase; font-weight: 700;
  padding: 5px 10px; border-radius: 999px; flex: none; }
.status.sealed { background: #e3d7c1; color: var(--ink-soft); border: 1px solid #cdb892; }
.status.open { background: var(--gold); color: #fffaf0; }
.lock-answer { margin: 0.1rem 0 0.2rem 56px; font-size: 0.92rem; color: var(--ink-soft); font-style: italic; }
.lock-miss { font-size: 0.88rem; color: #8c4a33; }

[data-testid="stForm"] { border: none; padding: 0; }
[data-testid="stTextInput"] input {
  background: #fffdf8; border: 1px solid var(--tan); border-radius: 12px; color: var(--ink);
  font-size: 1rem; padding: 0.6rem 0.9rem;
}
[data-testid="stTextInput"] input:focus { border-color: var(--gold); box-shadow: 0 0 0 3px rgba(185,143,78,0.2); }
[data-testid="stTextInput"] [data-baseweb="input"] { border: none; background: transparent; }
[data-testid="stTextInputRootElement"] { border: none !important; background: transparent !important; }

.yields { text-align: center; padding: 0.9rem 0 0.2rem; animation: rise .6s ease both; }
.yields h2 { font-size: 1.9rem; font-weight: 800; margin: 0; }
.yields p { color: var(--ink-soft); margin: 0.3rem 0 0; }

/* ---------- act 3 door ---------- */
.st-key-door-wrap {
  background: var(--cream); border: 1px solid var(--line); border-radius: 22px; padding: 1.6rem;
  box-shadow: 0 10px 30px -18px rgba(74,59,42,0.35); gap: 0.8rem;
}
.door-frame {
  width: 190px; height: 250px; margin: 0.3rem auto 0.6rem; position: relative;
  border-radius: 95px 95px 6px 6px; overflow: hidden;
  background: radial-gradient(ellipse at 50% 60%, #fff4d6, #f0d494 55%, #d8ac5e);
  box-shadow: 0 0 0 8px var(--tan), 0 0 0 9px #cdb892;
}
.door-frame.open { box-shadow: 0 0 0 8px var(--tan), 0 0 0 9px #cdb892, 0 0 50px 8px rgba(240,212,148,0.9); }
.leaf {
  position: absolute; top: 0; bottom: 0; width: 50%;
  background: repeating-linear-gradient(90deg, #8a6a43 0 22px, #7e603b 22px 24px);
  transition: transform .6s cubic-bezier(.3,.7,.2,1);
}
.leaf.l { left: 0; border-right: 1px solid #5c4529; }
.leaf.r { right: 0; border-left: 1px solid #5c4529; }
.leaf::after { content: ""; position: absolute; top: 55%; width: 9px; height: 9px; border-radius: 50%;
  background: var(--gold); box-shadow: 0 0 0 2px #5c4529; }
.leaf.l::after { right: 10px; } .leaf.r::after { left: 10px; }
.push-line { text-align: center; font-family: 'Fraunces', Georgia, serif; font-style: italic; font-size: 1.15rem; color: var(--ink-soft); min-height: 1.6rem; }
.pips { display: flex; justify-content: center; gap: 8px; margin: 0.2rem 0 0.2rem; }
.pips span { width: 34px; height: 8px; border-radius: 6px; background: var(--tan); opacity: .55; }
.pips span.on { background: var(--gold); opacity: 1; }
.pip-label { margin-bottom: 0.8rem; text-align: center; font-size: 0.78rem; letter-spacing: 0.08em; color: var(--ink-faint); }

/* ---------- victory ---------- */
.victory-top { text-align: center; padding: 1.2rem 0 0.6rem; }
.stamp {
  display: inline-block; font-family: 'Fraunces', Georgia, serif; font-weight: 900;
  font-size: 4.2rem; letter-spacing: 0.1em; color: var(--stamp);
  border: 5px double var(--stamp); border-radius: 12px; padding: 0.1rem 1.4rem 0.05rem 1.8rem;
  transform: rotate(-4deg); opacity: 0.9;
  animation: stamp .55s cubic-bezier(.2,1.4,.4,1) both;
  mix-blend-mode: multiply;
}
@keyframes stamp { from { transform: rotate(-4deg) scale(2.2); opacity: 0; } to { transform: rotate(-4deg) scale(1); opacity: 0.9; } }
.victory-top .sub { font-family: 'Fraunces', Georgia, serif; font-style: italic; color: var(--ink-soft); font-size: 1.2rem; margin-top: 1.1rem; }

.panel {
  background: var(--cream); border: 1px solid var(--line); border-radius: 22px; padding: 1.4rem 1.5rem;
  box-shadow: 0 10px 30px -18px rgba(74,59,42,0.35); animation: rise .5s ease both;
}
.panel-title { font-size: 0.74rem; letter-spacing: 0.26em; text-transform: uppercase; color: var(--gold-deep); font-weight: 700; margin-bottom: 0.7rem; }
.stat { display: flex; justify-content: space-between; align-items: baseline; padding: 0.55rem 0;
  border-bottom: 1px dashed var(--line); gap: 12px; }
.stat:last-child { border-bottom: none; }
.stat .k { color: var(--ink-soft); font-size: 0.98rem; }
.stat .v { font-family: 'Fraunces', Georgia, serif; font-weight: 700; font-size: 1.15rem; color: var(--ink); text-align: right; }

.section-title { text-align: center; margin: 2.2rem 0 1rem; }
.section-title .eyebrow { font-size: 0.74rem; letter-spacing: 0.26em; text-transform: uppercase; color: var(--gold-deep); font-weight: 700; }
.section-title h2 { font-size: 2rem; font-weight: 800; margin: 0.1rem 0 0; padding: 0; }
.section-title p { color: var(--ink-soft); margin: 0.3rem 0 0; }

[class*="st-key-quest-"] {
  background: var(--cream); border: 1px solid var(--line); border-radius: 22px;
  padding: 1.4rem 1.5rem 0.6rem; gap: 0.2rem; position: relative; overflow: hidden;
  box-shadow: 0 10px 30px -18px rgba(74,59,42,0.35);
}
[class*="st-key-quest-"]::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 6px;
  background: linear-gradient(var(--gold), var(--tan)); }
.quest-top { display: flex; justify-content: space-between; align-items: center; gap: 10px; flex-wrap: wrap; }
.quest-new { font-size: 0.66rem; letter-spacing: 0.16em; text-transform: uppercase; font-weight: 700;
  color: #fffaf0; background: var(--gold); padding: 4px 10px; border-radius: 999px; }
.quest-title { font-family: 'Fraunces', Georgia, serif; font-weight: 800; font-size: 1.75rem; color: var(--ink); margin: 0.5rem 0 0.35rem; line-height: 1.1; }
.quest-desc { font-size: 1.02rem; line-height: 1.6; margin: 0 0 0.8rem; color: var(--ink); }
.quest-detail { display: grid; grid-template-columns: 70px 1fr; gap: 4px 10px; font-size: 0.92rem; margin-bottom: 1rem; }
.quest-detail .k { font-size: 0.68rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--ink-faint); font-weight: 700; padding-top: 3px; }
.quest-detail .v { color: var(--ink-soft); }
.quest-link, .quest-link:visited { color: var(--gold-deep) !important; font-weight: 700; text-decoration: none;
  border-bottom: 1px solid var(--tan); transition: border-color .2s ease; }
.quest-link:hover { border-color: var(--gold-deep); }
.quest-link::after { content: " \\2197"; font-size: 0.85em; }

.closing { text-align: center; margin: 2.6rem auto 0; max-width: 480px; animation: rise .8s ease both; }
.closing p { font-family: 'Fraunces', Georgia, serif; font-size: 1.3rem; line-height: 1.55; color: var(--ink); }
.closing .sig { font-style: italic; color: var(--ink-soft); font-size: 1.1rem; margin-top: 0.6rem; }
.closing .save { margin-top: 1.8rem; display: inline-block; font-family: 'Nunito', 'Segoe UI', system-ui, sans-serif; font-size: 0.72rem;
  letter-spacing: 0.24em; text-transform: uppercase; font-weight: 700; color: var(--gold-deep);
  border: 1px solid var(--tan); padding: 8px 16px; border-radius: 999px; }
.closing .save .blink { animation: blink 1.2s steps(2) infinite; }
@keyframes blink { 50% { opacity: 0; } }

@media (max-width: 560px) {
  .intro h1 { font-size: 3.2rem; }
  .node-card { padding: 1.3rem 1.2rem 1.1rem; }
  .node-title { font-size: 1.6rem; }
  .stamp { font-size: 3rem; }
  .vault-head { padding: 0.4rem 2.4rem 0.2rem; }
  .vault-head h1 { font-size: 2rem; }
  .run-map .stop { min-width: 40px; font-size: 0.6rem; }
}
</style>
""".replace("BRICK_SVG", BRICK_SVG)


# =============================================================================
# 3. STATE AND NAVIGATION
# =============================================================================

STAGES = ["intro", "act1", "act2", "vault", "act3", "victory"]
MAP_STOPS = [("act1", "Act 1"), ("act2", "Act 2"), ("vault", "Vault"), ("act3", "Act 3"), ("victory", "Victory")]


def init_state():
    defaults = {
        "stage": "intro",
        "act1_idx": 0,
        "act2_idx": 0,
        "locks_open": [False] * len(VAULT_LOCKS),
        "lock_answers": [""] * len(VAULT_LOCKS),
        "lock_miss": [False] * len(VAULT_LOCKS),
        "pushes": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if st.session_state.stage not in STAGES:
        st.session_state.stage = "intro"


def go_to(stage):
    st.session_state.stage = stage


def act_next(act_key, total, next_stage):
    idx_key = f"{act_key}_idx"
    if st.session_state[idx_key] < total - 1:
        st.session_state[idx_key] += 1
    else:
        go_to(next_stage)


def act_back(act_key):
    idx_key = f"{act_key}_idx"
    st.session_state[idx_key] = max(0, st.session_state[idx_key] - 1)


def normalise(text):
    return " ".join(text.strip().lower().split())


def try_lock(i):
    guess = st.session_state.get(f"lock_input_{i}", "")
    expected = VAULT_LOCKS[i]["answer"]
    correct = bool(normalise(guess)) if expected is None else normalise(guess) == normalise(expected)
    if correct:
        st.session_state.locks_open[i] = True
        st.session_state.lock_answers[i] = guess.strip()
        st.session_state.lock_miss[i] = False
    else:
        st.session_state.lock_miss[i] = True


def restart_run():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_state()


def push_door():
    if st.session_state.pushes < PUSHES_NEEDED:
        st.session_state.pushes += 1


# =============================================================================
# 4. HELPERS
# =============================================================================

def esc(text):
    return html_lib.escape(text, quote=True)


def render(markup):
    """Render HTML through st.markdown. Lines are stripped so markdown never
    mistakes indented HTML for a code block."""
    flat = " ".join(line.strip() for line in markup.splitlines() if line.strip())
    st.markdown(flat, unsafe_allow_html=True)


PHOTO_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def find_photo(name):
    """Find a photo by name in the photos folder. Accepts the name with or
    without an extension, and ignores capitals."""
    if not name or not PHOTO_DIR.is_dir():
        return None
    target = name.lower()
    stem = Path(target).stem if Path(target).suffix in PHOTO_EXTS else target
    for path in sorted(PHOTO_DIR.iterdir()):
        if path.suffix.lower() in PHOTO_EXTS and (path.name.lower() == target or path.stem.lower() == stem):
            return path
    return None


def photo_html(name):
    path = find_photo(name)
    if path:
        mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
        data = base64.b64encode(path.read_bytes()).decode()
        return f'<div class="photo"><img src="data:{mime};base64,{data}" alt=""></div>'
    return '<div class="photo placeholder"><span>photo placeholder</span></div>'


def run_map():
    current = STAGES.index(st.session_state.stage)
    parts = []
    for n, (key, label) in enumerate(MAP_STOPS):
        pos = STAGES.index(key)
        state = "done" if pos < current else "here" if pos == current else ""
        if n > 0:
            parts.append(f'<div class="path {"done" if pos <= current else ""}"></div>')
        parts.append(f'<div class="stop {state}"><div class="pin"></div>{label}</div>')
    render(f'<div class="run-map">{"".join(parts)}</div>')


def act_header(eyebrow, title, sub):
    render(f"""
        <div class="act-head">
          <div class="eyebrow">{esc(eyebrow)}</div>
          <h1>{esc(title)}</h1>
          <p class="sub">{esc(sub)}</p>
        </div>
    """)


def progress_dots(idx, total, noun):
    dots = "".join(
        f'<span class="dot {"done" if i < idx else "now" if i == idx else ""}"></span>'
        for i in range(total)
    )
    render(f'<div class="dots">{dots}</div><div class="dots-label">{noun} {idx + 1} of {total}</div>')


def node_card(tag, date, title, photo, body, acquired):
    kind, _, name = acquired.partition(": ")
    date_html = f'<span class="node-date">{esc(date)}</span>' if date else ""
    render(f"""
        <div class="node-card">
          <div class="node-meta"><span class="tag">{esc(tag)}</span>{date_html}</div>
          <div class="node-title">{esc(title)}</div>
          {photo_html(photo)}
          <div class="node-body">{esc(body)}</div>
          <div class="acquired">
            <div class="gem"></div>
            <div><div class="kind">{esc(kind)}</div><div class="name">{esc(name)}</div></div>
          </div>
        </div>
    """)


def spacer():
    render('<div class="spacer"></div>')


def nav_buttons(act_key, idx, total, next_stage, last_label):
    label = last_label if idx == total - 1 else "Continue"
    if idx == 0:
        st.button(label, type="primary", key=f"{act_key}_next_{idx}",
                  on_click=act_next, args=(act_key, total, next_stage), width="stretch")
    else:
        back_col, next_col = st.columns([1, 2])
        with back_col:
            st.button("Back", key=f"{act_key}_back_{idx}", on_click=act_back, args=(act_key,), width="stretch")
        with next_col:
            st.button(label, type="primary", key=f"{act_key}_next_{idx}",
                      on_click=act_next, args=(act_key, total, next_stage), width="stretch")


def countdown(start_iso, end_iso):
    components.html(f"""
<!doctype html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700&family=Nunito:wght@700&display=swap" rel="stylesheet">
<style>
  html, body {{ margin: 0; background: transparent; font-family: 'Nunito', 'Segoe UI', system-ui, sans-serif; }}
  .row {{ display: flex; gap: 8px; }}
  .box {{ flex: 1; background: #f4ede1; border: 1px solid #e4d2ac; border-radius: 14px;
          text-align: center; padding: 10px 4px 8px; }}
  .num {{ font-family: 'Fraunces', Georgia, serif; font-weight: 700; font-size: 26px; color: #4a3b2a; line-height: 1; }}
  .lab {{ font-size: 10px; letter-spacing: .18em; text-transform: uppercase; color: #9a8567; margin-top: 6px; }}
  .live {{ display: none; background: #b98f4e; color: #fffaf0; border-radius: 14px; text-align: center;
           padding: 18px 10px; font-family: 'Fraunces', Georgia, serif; font-size: 20px; font-weight: 700; }}
</style></head><body>
<div class="row" id="row">
  <div class="box"><div class="num" id="d">0</div><div class="lab">days</div></div>
  <div class="box"><div class="num" id="h">00</div><div class="lab">hours</div></div>
  <div class="box"><div class="num" id="m">00</div><div class="lab">mins</div></div>
  <div class="box"><div class="num" id="s">00</div><div class="lab">secs</div></div>
</div>
<div class="live" id="live"></div>
<script>
  const start = new Date("{start_iso}").getTime();
  const end = new Date("{end_iso}").getTime();
  const pad = n => String(n).padStart(2, "0");
  function tick() {{
    const now = Date.now();
    let diff = start - now;
    if (diff <= 0) {{
      document.getElementById("row").style.display = "none";
      const live = document.getElementById("live");
      live.style.display = "block";
      live.textContent = now < end ? "Quest in progress" : "Quest complete";
      return;
    }}
    const s = Math.floor(diff / 1000);
    document.getElementById("d").textContent = Math.floor(s / 86400);
    document.getElementById("h").textContent = pad(Math.floor(s % 86400 / 3600));
    document.getElementById("m").textContent = pad(Math.floor(s % 3600 / 60));
    document.getElementById("s").textContent = pad(s % 60);
  }}
  tick();
  setInterval(tick, 1000);
</script>
</body></html>
""", height=82)


def popper():
    """One confetti burst from both bottom corners, drawn over the whole page.
    Fires once each time the victory screen is reached."""
    components.html("""
<script>
(function () {
  let doc;
  try { doc = window.parent.document; doc.body; } catch (e) { return; }
  if (window.parent.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const canvas = doc.createElement("canvas");
  canvas.style.cssText = "position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;z-index:99999";
  doc.body.appendChild(canvas);
  const ctx = canvas.getContext("2d");
  const W = canvas.width = window.parent.innerWidth;
  const H = canvas.height = window.parent.innerHeight;
  const colours = ["#b98f4e", "#e4d2ac", "#9c7538", "#fbf6ec", "#a4553a", "#d8b77a"];
  const bits = [];
  function burst(x, dir) {
    for (let i = 0; i < 90; i++) {
      const angle = (dir > 0 ? -Math.PI / 3 : -2 * Math.PI / 3) + (Math.random() - 0.5) * 0.9;
      const speed = 9 + Math.random() * 11;
      bits.push({
        x: x, y: H + 10,
        vx: Math.cos(angle) * speed, vy: Math.sin(angle) * speed * 1.35,
        w: 6 + Math.random() * 6, h: 3 + Math.random() * 5,
        r: Math.random() * Math.PI, vr: (Math.random() - 0.5) * 0.35,
        c: colours[Math.floor(Math.random() * colours.length)],
        round: Math.random() < 0.3
      });
    }
  }
  burst(0, 1);
  burst(W, -1);
  const start = performance.now();
  function frame(now) {
    const t = now - start;
    ctx.clearRect(0, 0, W, H);
    ctx.globalAlpha = t > 2600 ? Math.max(0, 1 - (t - 2600) / 900) : 1;
    for (const b of bits) {
      b.vy += 0.32; b.vx *= 0.985; b.vy *= 0.985;
      b.x += b.vx; b.y += b.vy; b.r += b.vr;
      ctx.save(); ctx.translate(b.x, b.y); ctx.rotate(b.r); ctx.fillStyle = b.c;
      if (b.round) { ctx.beginPath(); ctx.arc(0, 0, b.h, 0, Math.PI * 2); ctx.fill(); }
      else { ctx.fillRect(-b.w / 2, -b.h / 2, b.w, b.h * Math.abs(Math.cos(b.r))); }
      ctx.restore();
    }
    if (t < 3500) requestAnimationFrame(frame); else canvas.remove();
  }
  setTimeout(() => requestAnimationFrame(frame), 350);
})();
</script>
""", height=0)


# =============================================================================
# 5. SCREENS
# =============================================================================

def screen_intro():
    render(f"""
        <div class="intro">
          <div class="crest"><div></div></div>
          <div class="eyebrow">A birthday run for {esc(HIS_NAME)}</div>
          <h1>The Run</h1>
          <div class="lede">You have played this one before.</div>
          <div class="copy">
            Every node on this map is somewhere we have already been. Every relic is
            something you already earned. You just did not know you were playing.
            <br><br>
            Something is waiting for you at the very end. You have to earn it first.
          </div>
          <div class="rules">One life &nbsp;&middot;&nbsp; No skipping &nbsp;&middot;&nbsp; Good luck</div>
        </div>
    """)
    left, mid, right = st.columns([1, 2, 1])
    with mid:
        st.button("Begin the run", type="primary", key="start", on_click=go_to, args=("act1",), width="stretch")


def screen_act1():
    run_map()
    act_header("Act 1", "The Beginning", "Where it all started.")
    idx = st.session_state.act1_idx
    total = len(ACT1_NODES)
    progress_dots(idx, total, "Node")
    node = ACT1_NODES[idx]
    node_card(node["tag"], node["date"], node["title"], node["photo"], node["body"], node["acquired"])
    spacer()
    nav_buttons("act1", idx, total, "act2", "Continue to Act 2")


def screen_act2():
    run_map()
    act_header("Act 2", "The Grind", "Relics picked up along the way.")
    idx = st.session_state.act2_idx
    total = len(ACT2_NODES)
    progress_dots(idx, total, "Relic")
    node = ACT2_NODES[idx]
    node_card("Relic", f"{idx + 1} of {total}", node["title"], node["photo"], node["body"], node["acquired"])
    spacer()
    nav_buttons("act2", idx, total, "vault", "Continue to the Vault")


def screen_vault():
    run_map()
    numerals = ["I", "II", "III", "IV", "V"]
    with st.container(key="vault"):
        torch = '<div class="flame"></div><div class="stick"></div>'
        render(f"""
            <div class="vault-head">
              <div class="torch l">{torch}</div>
              <div class="torch r">{torch}</div>
              <div class="eyebrow">Deep below the bank</div>
              <h1>The Vault</h1>
              <p class="sub">Prove you know her.</p>
              <p class="blurb">Three locks. Each one only opens for someone who really knows her.
              Guess wrong and the vault just waits.</p>
            </div>
        """)

        for i, lock in enumerate(VAULT_LOCKS):
            is_open = st.session_state.locks_open[i]
            with st.container(key=f"lock-{i}"):
                status = '<span class="status open">Unlocked</span>' if is_open else '<span class="status sealed">Locked</span>'
                render(f"""
                    <div class="lock-row">
                      <div class="keyhole {"open" if is_open else ""}"></div>
                      <div class="lock-text">
                        <div class="lock-num">Lock {numerals[i]}</div>
                        <div class="lock-q">{esc(lock["question"])}</div>
                      </div>
                      {status}
                    </div>
                """)
                if is_open:
                    render(f'<div class="lock-answer">You said "{esc(st.session_state.lock_answers[i])}". The lock gives way.</div>')
                else:
                    with st.form(key=f"lock_form_{i}", clear_on_submit=False, border=False):
                        st.text_input("Your answer", key=f"lock_input_{i}",
                                      label_visibility="collapsed", placeholder="Your answer")
                        st.form_submit_button("Try the lock", on_click=try_lock, args=(i,), width="stretch")
                    if st.session_state.lock_miss[i]:
                        render('<div class="lock-miss">The lock does not budge. Try again.</div>')

        if all(st.session_state.locks_open):
            render("""
                <div class="yields">
                  <h2>The vault yields.</h2>
                  <p>Every lock is open. Whatever is inside was always meant for you.</p>
                </div>
            """)
            left, mid, right = st.columns([1, 2, 1])
            with mid:
                st.button("Step inside", type="primary", key="vault_enter", on_click=go_to, args=("act3",), width="stretch")


def screen_act3():
    run_map()
    act_header("Act 3", "One Last Thing", "You already proved yourself in the vault. This is just the door.")
    pushes = st.session_state.pushes
    done = pushes >= PUSHES_NEEDED
    shift = int(pushes / PUSHES_NEEDED * 100)
    with st.container(key="door-wrap"):
        line = "The door is open." if done else PUSH_LINES[min(pushes, len(PUSH_LINES) - 1)]
        pips = "".join(f'<span class="{"on" if i < pushes else ""}"></span>' for i in range(PUSHES_NEEDED))
        render(f"""
            <div class="door-frame {"open" if done else ""}">
              <div class="leaf l" style="transform: translateX(-{shift}%);"></div>
              <div class="leaf r" style="transform: translateX({shift}%);"></div>
            </div>
            <div class="push-line">{esc(line)}</div>
            <div class="pips">{pips}</div>
            <div class="pip-label">{pushes} of {PUSHES_NEEDED} pushes</div>
        """)
        left, mid, right = st.columns([1, 2, 1])
        with mid:
            if done:
                st.button("Walk through", type="primary", key="walk", on_click=go_to, args=("victory",), width="stretch")
            else:
                st.button("Push", type="primary", key="push", on_click=push_door, width="stretch")


def screen_victory():
    popper()
    render("""
        <div class="victory-top">
          <div class="stamp">VICTORY</div>
          <div class="sub">Run complete. Well played.</div>
        </div>
    """)
    stats = [
        ("Relics collected", str(len(ACT2_NODES))),
        ("Story nodes cleared", str(len(ACT1_NODES))),
        ("Vault", "Cracked"),
        ("Final door", "Opened"),
        ("Run started", RUN_STARTED),
    ]
    rows = "".join(f'<div class="stat"><span class="k">{k}</span><span class="v">{v}</span></div>' for k, v in stats)
    render(f'<div class="panel"><div class="panel-title">Run stats</div>{rows}</div>')

    render("""
        <div class="section-title">
          <div class="eyebrow">Reward</div>
          <h2>New quests unlocked</h2>
          <p>Both on the same day. Scent first, then the feast.</p>
        </div>
    """)
    for q in QUESTS:
        with st.container(key=f"quest-{q['key']}"):
            render(f"""
                <div class="quest-top">
                  <span class="tag">{esc(q["number"])}</span>
                  <span class="quest-new">Unlocked</span>
                </div>
                <div class="quest-title">{esc(q["title"])}</div>
                <p class="quest-desc">{esc(q["desc"])}</p>
                <div class="quest-detail">
                  <span class="k">When</span><span class="v">{esc(q["when"])}</span>
                  <span class="k">Where</span><span class="v">{esc(q["where"])}</span>
                  <span class="k">Peek</span><span class="v"><a class="quest-link" href="{esc(q["link"])}" target="_blank" rel="noopener">Check them out on Instagram</a></span>
                </div>
            """)
            countdown(q["start_iso"], q["end_iso"])
        spacer()

    render(f"""
        <div class="closing">
          <p>Thank you for playing through this whole run with me, even before you knew you were doing it.</p>
          <div class="sig">Happy birthday. Love, {esc(HER_NAME)}</div>
          <div class="save">New save file starting soon<span class="blink">_</span></div>
        </div>
    """)
    render('<div class="spacer"></div><div class="spacer"></div>')
    left, mid, right = st.columns([1, 2, 1])
    with mid:
        st.button("Play the run again", key="rerun", on_click=restart_run, width="stretch")


# =============================================================================
# 6. ROUTER
# =============================================================================

st.set_page_config(page_title="The Run", page_icon=None, layout="centered", initial_sidebar_state="collapsed")
st.markdown("\n".join(line for line in CSS.splitlines() if line.strip()), unsafe_allow_html=True)
init_state()

SCREENS = {
    "intro": screen_intro,
    "act1": screen_act1,
    "act2": screen_act2,
    "vault": screen_vault,
    "act3": screen_act3,
    "victory": screen_victory,
}
SCREENS[st.session_state.stage]()

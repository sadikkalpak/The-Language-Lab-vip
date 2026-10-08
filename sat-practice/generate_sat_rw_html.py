#!/usr/bin/env python3
"""Generate interactive HTML SAT R&W practice test from shared QUESTIONS."""

import html as htmlmod
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "SAT_Reading_Writing_Practice_Test_30.html"


def load_questions():
    spec = importlib.util.spec_from_file_location("gen", HERE / "generate_sat_rw_test.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert len(mod.QUESTIONS) == 30
    return mod.QUESTIONS


def build_html(questions):
    items_html = []
    for i, q in enumerate(questions, 1):
        passage = ""
        if q.get("passage"):
            passage = f'<div class="passage">{q["passage"]}</div>'
        choices = []
        for ch in q["choices"]:
            letter = ch[0]
            text = ch[3:] if ch[1:3] == ") " else ch
            choices.append(
                f'<label class="choice"><input type="radio" name="q{i}" value="{letter}">'
                f'<span class="bubble">{letter}</span>'
                f'<span class="choice-text">{text}</span></label>'
            )
        items_html.append(
            f"""
    <article class="question" data-num="{i}" data-answer="{q["answer"]}" data-explain="{htmlmod.escape(q["explain"])}">
      <div class="q-head">
        <span class="q-num">Question {i}</span>
        <span class="topic">{htmlmod.escape(q["topic"])}</span>
      </div>
      {passage}
      <p class="stem">{q["stem"]}</p>
      <div class="choices">{"".join(choices)}</div>
      <div class="feedback" hidden></div>
    </article>"""
        )

    answers_js = ", ".join(f'"{q["answer"]}"' for q in questions)

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SAT Reading &amp; Writing Practice Test — 30 Questions</title>
<style>
:root {{
  --ink: #1a2332;
  --muted: #5a6570;
  --line: #d8dee6;
  --paper: #f6f3ee;
  --card: #ffffff;
  --navy: #1e3a5f;
  --teal: #2f6f6d;
  --ok: #166534;
  --ok-bg: #dcfce7;
  --bad: #991b1b;
  --bad-bg: #fee2e2;
  --shadow: 0 1px 0 rgba(30,58,95,.06), 0 12px 32px rgba(30,58,95,.08);
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  color: var(--ink);
  background:
    radial-gradient(900px 420px at 10% -10%, #dfe9f2 0%, transparent 55%),
    radial-gradient(700px 380px at 100% 0%, #e7efe9 0%, transparent 50%),
    var(--paper);
  line-height: 1.5;
}}
.wrap {{
  max-width: 720px;
  margin: 0 auto;
  padding: 2rem 1.25rem 4rem;
}}
header.hero {{
  text-align: center;
  padding: 2.2rem 1.5rem 1.8rem;
  background: linear-gradient(160deg, #1e3a5f 0%, #2f6f6d 100%);
  color: #f8fafc;
  border-radius: 18px;
  box-shadow: var(--shadow);
  margin-bottom: 1.5rem;
}}
header.hero .eyebrow {{
  letter-spacing: .12em;
  text-transform: uppercase;
  font-size: .75rem;
  opacity: .85;
  margin: 0 0 .5rem;
}}
header.hero h1 {{
  font-family: Georgia, "Times New Roman", Times, serif;
  font-weight: 600;
  font-size: clamp(1.6rem, 4vw, 2.2rem);
  margin: 0 0 .35rem;
  line-height: 1.2;
}}
header.hero .sub {{
  margin: 0;
  opacity: .92;
  font-size: 1.05rem;
}}
.meta {{
  display: flex;
  flex-wrap: wrap;
  gap: .6rem;
  justify-content: center;
  margin-top: 1.1rem;
}}
.meta span {{
  background: rgba(255,255,255,.14);
  border: 1px solid rgba(255,255,255,.22);
  padding: .35rem .7rem;
  border-radius: 999px;
  font-size: .85rem;
}}
.panel {{
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 1.1rem 1.25rem;
  margin-bottom: 1.25rem;
  box-shadow: var(--shadow);
}}
.panel h2 {{
  font-family: Georgia, "Times New Roman", Times, serif;
  font-size: 1.15rem;
  margin: 0 0 .6rem;
  color: var(--navy);
}}
.panel p, .panel li {{ color: var(--muted); font-size: .95rem; }}
.panel ul {{ margin: .4rem 0 0; padding-left: 1.2rem; }}
.toolbar {{
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  flex-wrap: wrap;
  gap: .6rem;
  align-items: center;
  justify-content: space-between;
  background: rgba(246,243,238,.92);
  backdrop-filter: blur(8px);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: .7rem .9rem;
  margin-bottom: 1.25rem;
}}
.progress {{
  font-size: .9rem;
  color: var(--muted);
  font-weight: 600;
}}
.btn {{
  appearance: none;
  border: none;
  cursor: pointer;
  font: inherit;
  font-weight: 700;
  border-radius: 10px;
  padding: .55rem 1rem;
  background: var(--navy);
  color: white;
}}
.btn:hover {{ filter: brightness(1.08); }}
.btn.secondary {{
  background: white;
  color: var(--navy);
  border: 1px solid var(--line);
}}
.question {{
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 1.15rem 1.25rem 1.25rem;
  margin-bottom: 1rem;
  box-shadow: var(--shadow);
}}
.question.correct {{ border-color: #86efac; }}
.question.wrong {{ border-color: #fca5a5; }}
.q-head {{
  display: flex;
  flex-wrap: wrap;
  gap: .5rem .85rem;
  align-items: baseline;
  margin-bottom: .65rem;
}}
.q-num {{ font-weight: 700; color: var(--navy); }}
.topic {{
  font-size: .78rem;
  color: var(--teal);
  font-style: italic;
}}
.passage {{
  font-family: Georgia, "Times New Roman", Times, serif;
  background: #f0f4f8;
  border-left: 3px solid var(--teal);
  padding: .85rem 1rem;
  margin: 0 0 .85rem;
  border-radius: 0 10px 10px 0;
  font-size: .98rem;
}}
.stem {{ margin: 0 0 .7rem; font-weight: 600; }}
.choices {{ display: grid; gap: .45rem; }}
.choice {{
  display: flex;
  gap: .65rem;
  align-items: flex-start;
  padding: .55rem .7rem;
  border: 1px solid var(--line);
  border-radius: 10px;
  cursor: pointer;
  background: #fff;
}}
.choice:hover {{ border-color: #9db4cc; background: #f8fafc; }}
.choice:has(input:checked) {{
  border-color: var(--teal);
  background: #eef6f5;
}}
.choice input {{ position: absolute; opacity: 0; pointer-events: none; }}
.bubble {{
  flex: 0 0 1.55rem;
  width: 1.55rem;
  height: 1.55rem;
  border-radius: 50%;
  border: 1.5px solid var(--navy);
  display: grid;
  place-items: center;
  font-size: .8rem;
  font-weight: 700;
  color: var(--navy);
  margin-top: .05rem;
}}
.choice:has(input:checked) .bubble {{
  background: var(--teal);
  border-color: var(--teal);
  color: white;
}}
.choice-text {{ flex: 1; padding-top: .1rem; }}
.feedback {{
  margin-top: .85rem;
  padding: .7rem .85rem;
  border-radius: 10px;
  font-size: .92rem;
}}
.feedback.ok {{ background: var(--ok-bg); color: var(--ok); }}
.feedback.bad {{ background: var(--bad-bg); color: var(--bad); }}
#results {{ display: none; text-align: center; }}
#results.show {{ display: block; }}
#results .score {{
  font-family: Georgia, "Times New Roman", Times, serif;
  font-size: 2.4rem;
  font-weight: 600;
  color: var(--navy);
  margin: .2rem 0;
}}
footer.note {{
  margin-top: 2rem;
  text-align: center;
  font-size: .8rem;
  color: var(--muted);
}}
@media print {{
  body {{ background: white; }}
  .toolbar, .btn, header.hero .meta {{ display: none !important; }}
  .question {{ break-inside: avoid; box-shadow: none; }}
}}
</style>
</head>
<body>
  <div class="wrap">
    <header class="hero">
      <p class="eyebrow">Digital SAT® Style</p>
      <h1>Reading and Writing</h1>
      <p class="sub">30 Soruluk Alıştırma Sınavı · İlk / Temel Konular</p>
      <div class="meta">
        <span>30 soru</span>
        <span>~32 dakika</span>
        <span>A · B · C · D</span>
      </div>
    </header>

    <section class="panel">
      <h2>Yönergeler / Directions</h2>
      <p>Her sorunun bir doğru cevabı vardır. Cevaplarını seç, bitince <strong>Kontrol et</strong>e bas.</p>
      <p>Each question has one best answer. Select your choices, then click <strong>Check answers</strong>.</p>
      <ul>
        <li>1–5 Words in Context</li>
        <li>6–9 Central Ideas &amp; Details · 10–12 Inferences · 13–15 Evidence</li>
        <li>16–17 Structure &amp; Purpose · 18–20 Transitions · 21 Rhetorical Synthesis</li>
        <li>22–25 Boundaries · 26–30 Form, Structure &amp; Sense</li>
      </ul>
    </section>

    <div class="toolbar">
      <div class="progress"><span id="answered">0</span> / 30 answered</div>
      <div style="display:flex;gap:.5rem;flex-wrap:wrap">
        <button type="button" class="btn secondary" id="resetBtn">Sıfırla</button>
        <button type="button" class="btn" id="checkBtn">Kontrol et</button>
      </div>
    </div>

    <form id="testForm">
{"".join(items_html)}
    </form>

    <section class="panel" id="results">
      <h2>Sonuç / Results</h2>
      <p class="score" id="scoreText">0 / 30</p>
      <p id="scoreNote" style="color:var(--muted)"></p>
      <button type="button" class="btn secondary" id="showKeyBtn" style="margin-top:.5rem">Cevap anahtarını göster</button>
      <div id="answerKey" hidden style="text-align:left;margin-top:1rem"></div>
    </section>

    <footer class="note">
      Unofficial practice material · Digital SAT® is a trademark of College Board.
    </footer>
  </div>

<script>
const ANSWERS = [{answers_js}];
const form = document.getElementById('testForm');
const answeredEl = document.getElementById('answered');
const results = document.getElementById('results');
const scoreText = document.getElementById('scoreText');
const scoreNote = document.getElementById('scoreNote');
const answerKey = document.getElementById('answerKey');

function countAnswered() {{
  let n = 0;
  for (let i = 1; i <= 30; i++) {{
    if (form.querySelector(`input[name="q${{i}}"]:checked`)) n++;
  }}
  answeredEl.textContent = n;
}}

form.addEventListener('change', countAnswered);

document.getElementById('checkBtn').addEventListener('click', () => {{
  let correct = 0;
  const articles = form.querySelectorAll('.question');
  articles.forEach((art, idx) => {{
    const ans = art.dataset.answer;
    const picked = form.querySelector(`input[name="q${{idx + 1}}"]:checked`);
    const fb = art.querySelector('.feedback');
    art.classList.remove('correct', 'wrong');
    fb.hidden = false;
    if (picked && picked.value === ans) {{
      correct++;
      art.classList.add('correct');
      fb.className = 'feedback ok';
      fb.textContent = `Doğru · ${{ans}}. ${{art.dataset.explain}}`;
    }} else {{
      art.classList.add('wrong');
      fb.className = 'feedback bad';
      const yours = picked ? picked.value : '—';
      fb.textContent = `Yanlış (senin: ${{yours}}, doğru: ${{ans}}). ${{art.dataset.explain}}`;
    }}
  }});
  results.classList.add('show');
  scoreText.textContent = `${{correct}} / 30`;
  const pct = Math.round((correct / 30) * 100);
  scoreNote.textContent = pct >= 80
    ? `Harika iş — %${{pct}}. Temel konular güçlü görünüyor.`
    : pct >= 60
      ? `İyi başlangıç — %${{pct}}. Yanlışları gözden geçir.`
      : `%${{pct}}. Cevap anahtarı ve açıklamalarla tekrar et.`;
  results.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
}});

document.getElementById('resetBtn').addEventListener('click', () => {{
  form.reset();
  form.querySelectorAll('.question').forEach(art => {{
    art.classList.remove('correct', 'wrong');
    const fb = art.querySelector('.feedback');
    fb.hidden = true;
    fb.textContent = '';
  }});
  results.classList.remove('show');
  answerKey.hidden = true;
  answerKey.innerHTML = '';
  countAnswered();
  window.scrollTo({{ top: 0, behavior: 'smooth' }});
}});

document.getElementById('showKeyBtn').addEventListener('click', () => {{
  if (!answerKey.hidden && answerKey.innerHTML) {{
    answerKey.hidden = true;
    return;
  }}
  answerKey.innerHTML = ANSWERS.map((a, i) => `<strong>${{i + 1}}.</strong> ${{a}}`).join(' &nbsp;&nbsp; ');
  answerKey.hidden = false;
}});
</script>
</body>
</html>
"""


def main():
    questions = load_questions()
    OUTPUT.write_text(build_html(questions), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()

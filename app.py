"""Prithvi's Story World: storytelling and multiplication practice."""
from pathlib import Path
import random

import streamlit as st
from data.story_data import HINTS, PROMPTS, vocabulary_for

BASE = Path(__file__).resolve().parent
CATEGORIES = list(PROMPTS)
COLORS = ["#f6a6c8", "#c1b8fa", "#a7d8e8", "#aedcc6", "#f7d59a", "#eeb6a6", "#a8d6f1", "#e4b7df", "#b9d897", "#f5c78e"]
TABLE_ORDER = [7, 8, 12, 3, 6, 9, 11, 2, 4, 5]
STEPS = [
    ("👧", "Choose your characters", "Who is your hero? What do they want? What makes them interesting?"),
    ("🏡", "Imagine the setting", "Where and when does your story happen? What can you see, hear, or feel there?"),
    ("🌅", "Plan the beginning", "What is happening at first? What unexpected event starts your story?"),
    ("🧩", "Introduce a problem", "What gets in your hero's way? Why does this challenge matter?"),
    ("✨", "Create a surprising twist", "What happens that nobody expects? How does the hero respond?"),
    ("🌈", "Decide the ending", "How is the challenge resolved? How has your hero changed?"),
]
st.set_page_config(page_title="Prithvi's Story World", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")


def go(page):
    st.session_state.page = page
    st.rerun()


def new_story():
    st.session_state.selected = None
    st.session_state.spinning = False
    st.session_state.planner_step = 0
    st.session_state.plan_answers = {}
    for i in range(6):
        st.session_state.pop(f"plan_{i}", None)
        st.session_state.pop(f"plan_widget_{i}", None)


def new_quiz():
    """Create ten different questions from the 2–12 times tables (× 1–10)."""
    questions = [(a, b) for a in range(2, 13) for b in range(1, 11)]
    st.session_state.math_questions = random.sample(questions, 10)
    st.session_state.math_index = 0
    st.session_state.math_results = []
    st.session_state.pop("math_answer", None)


def math_tables():
    st.markdown('<h1>✖️ Multiplication Fun!</h1>', unsafe_allow_html=True)
    st.markdown('<p class="intro">Practise these ten tables, each up to × 10. When you feel ready, try ten fun questions!</p>', unsafe_allow_html=True)
    for row_start in (0, 5):
        cols = st.columns(5, gap="small")
        for number, col in zip(TABLE_ORDER[row_start:row_start + 5], cols):
            with col:
                with st.container(border=True):
                    st.markdown(f"<div class='math-table-heading'>× {number}</div>", unsafe_allow_html=True)
                    for multiplier in range(1, 11):
                        st.markdown(f"<div class='math-table-line'>{number} × {multiplier} = <strong>{number * multiplier}</strong></div>", unsafe_allow_html=True)
    if st.button("🚀 Start my 10-question challenge!", type="primary", use_container_width=True):
        new_quiz()
        go("math_quiz")
    if st.button("🏠 Back to home", use_container_width=True):
        go("welcome")


def math_quiz():
    if "math_questions" not in st.session_state:
        new_quiz()
    index = st.session_state.math_index
    if index >= 10:
        go("math_results")
    a, b = st.session_state.math_questions[index]
    st.markdown('<h1>🧠 Multiplication Challenge</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="step-counter">Question {index + 1} of 10</p>', unsafe_allow_html=True)
    st.progress((index + 1) / 10)
    st.markdown(f'<div class="math-question">{a} × {b} = ?</div>', unsafe_allow_html=True)
    with st.form(key=f"question_{index}", clear_on_submit=False):
        answer = st.number_input("Your answer", min_value=0, max_value=1200, value=None,
                                 step=1, placeholder="Type your answer", key=f"math_answer_{index}")
        submitted = st.form_submit_button("Next question →" if index < 9 else "🏆 Finish challenge!",
                                          type="primary", use_container_width=True)
    if submitted:
        if answer is None:
            st.warning("Type an answer first. Take your time! 💜")
        else:
            correct = a * b
            st.session_state.math_results.append({"a": a, "b": b, "answer": int(answer),
                                                  "correct": correct, "is_correct": answer == correct})
            st.session_state.math_index += 1
            go("math_results" if index == 9 else "math_quiz")


def math_results():
    results = st.session_state.get("math_results", [])
    if len(results) != 10:
        go("math_tables")
    score = sum(item["is_correct"] for item in results)
    if score == 10:
        message = "WOW, Prithvi! You're a multiplication superstar! 🌟"
    elif score >= 8:
        message = "Amazing work! You're getting stronger with every question! 🌷"
    elif score >= 5:
        message = "Great effort! Every question you try makes your brain stronger! 💖"
    elif score >= 2:
        message = "I'm proud of you for trying! Mistakes help us learn. Keep going! 🌈"
    else:
        message = "You showed up and gave it a try! Let's learn together, one step at a time! ❤️"
    st.markdown(
        f'<div class="math-results-header"><div class="math-results-title">🏆 Great Job, Prithvi!</div>'
        f'<div class="math-score">{score} / 10</div>'
        f'<div class="math-results-cheer">{message}</div></div>',
        unsafe_allow_html=True,
    )
    tiles = []
    for number, item in enumerate(results, start=1):
        is_correct = item["is_correct"]
        result_label = "✅ Correct!" if is_correct else "❌ Wrong"
        answer_line = (
            f'<div class="math-tile-answer">Your answer: <strong>{item["answer"]}</strong></div>'
        )
        correction = (
            "" if is_correct else
            f'<div class="math-tile-correction">Correct: <strong>{item["correct"]}</strong></div>'
        )
        tiles.append(
            f'<div class="math-result-tile {"math-tile-right" if is_correct else "math-tile-wrong"}">'
            f'<div class="math-tile-number">Question {number}</div>'
            f'<div class="math-tile-problem">{item["a"]} × {item["b"]} = {item["correct"] if is_correct else "?"}</div>'
            f'<div class="math-tile-status">{result_label}</div>'
            f'{answer_line}{correction}</div>'
        )
    st.markdown('<div class="math-results-grid">' + ''.join(tiles) + '</div>', unsafe_allow_html=True)
    again, tables, home = st.columns(3, gap="small")
    with again:
        if st.button("🔄 Practice again", type="primary", use_container_width=True):
            new_quiz()
            go("math_quiz")
    with tables:
        if st.button("📚 Review tables", use_container_width=True):
            go("math_tables")
    with home:
        if st.button("🏠 Home", use_container_width=True):
            go("welcome")


def welcome():
    picture, words = st.columns([1, 1.25], gap="medium", vertical_alignment="center")
    with picture:
        st.image(str(BASE / "assets/prithvi_kawaii.png"), width=300)
    with words:
        st.markdown("<h1>Hello, Prithvi! 🌸</h1>", unsafe_allow_html=True)
        st.markdown('<div class="quote">“Your imagination is your superpower. There is no wrong way to begin a story.”</div>', unsafe_allow_html=True)
        if st.button("✨ Let’s create a story!", type="primary", use_container_width=True):
            go("wheel")
        if st.button("✖️ Multiplication Fun!", key="multiplication_home", use_container_width=True):
            go("math_tables")
        st.markdown('<p class="footer-note">Made with love for a curious young storyteller 💜</p>', unsafe_allow_html=True)


def wheel():
    st.markdown('<h1>🎡 The Magic Story Wheel</h1>', unsafe_allow_html=True)
    gradient = ",".join(f"{c} {i*10}% {(i+1)*10}%" for i, c in enumerate(COLORS))
    spinning = st.session_state.spinning
    rotation = -(st.session_state.wheel_index * 36 + 18)
    motion = "animation: spin 1.25s linear infinite;" if spinning else f"transform:rotate({rotation}deg);"
    left, right = st.columns([1, 1.2], gap="large", vertical_alignment="center")
    with left:
        st.markdown(f'<div class="wheel-area"><div class="pointer">▼</div><div class="wheel" style="background:conic-gradient({gradient});{motion}"><div class="wheel-center">✨</div></div></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<p class="intro">Ten wonderful worlds and one hundred story possibilities. Ready, Prithvi?</p>', unsafe_allow_html=True)
        if not st.session_state.selected and not spinning:
            if st.button("🎡 Spin the wheel!", type="primary", use_container_width=True):
                st.session_state.spinning = True
                st.rerun()
        elif not st.session_state.selected:
            st.success("It's spinning! Press Stop whenever you're ready.")
            if st.button("🛑 STOP the wheel", type="primary", use_container_width=True):
                idx = random.randrange(10)
                cat = CATEGORIES[idx]
                title, premise = random.choice(PROMPTS[cat])
                st.session_state.selected = dict(category=cat, title=title, premise=premise, hints=HINTS[cat])
                st.session_state.wheel_index = idx
                st.session_state.spinning = False
                st.rerun()
        else:
            st.success(f"🎉 Your wheel landed on **{st.session_state.selected['category']}**!")
            if st.button("✨ Discover my story!", type="primary", use_container_width=True):
                go("prompt")
            if st.button("🔄 Spin again", use_container_width=True):
                new_story()
                st.rerun()
    st.caption("Categories: " + " · ".join(CATEGORIES))


def prompt():
    story = st.session_state.selected
    st.markdown(f"<h1>{story['title']}</h1>", unsafe_allow_html=True)
    left, right = st.columns(2, gap="large")
    with left:
        st.info(f"🎨 Story world: **{story['category']}**")
        st.markdown(f"<p class='intro'>{story['premise']} What happens next is completely up to you!</p>", unsafe_allow_html=True)
        st.markdown('<div class="quote">“Your ideas make the story yours!”</div>', unsafe_allow_html=True)
    with right:
        st.subheader("💡 Three imagination sparks")
        for n, hint in enumerate(story["hints"], 1):
            st.markdown(f"**{n}.** {hint}")
    if st.button("📝 Let's plan my story", type="primary", use_container_width=True):
        go("planner")
    if st.button("← Back to wheel", use_container_width=True):
        go("wheel")


def planner():
    step = st.session_state.setdefault("planner_step", 0)
    answers = st.session_state.setdefault("plan_answers", {})
    emoji, title, question = STEPS[step]

    st.markdown('<h1>📝 My Story Blueprint</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="step-counter">Step {step+1} of 6</p>', unsafe_allow_html=True)
    st.progress((step + 1) / len(STEPS))
    widget_key = f"plan_widget_{step}"
    if widget_key not in st.session_state:
        st.session_state[widget_key] = answers.get(step, "")

    def keep_answer(index=step, key=widget_key):
        st.session_state.plan_answers[index] = st.session_state[key]

    left, right = st.columns([1, 1.2], gap="large", vertical_alignment="center")
    with left:
        st.markdown(f'<div class="step-illustration">{emoji}</div>', unsafe_allow_html=True)
        st.markdown(f'### {title}')
        st.write(question)
        st.caption("A few words or big ideas are both wonderful!")
    with right:
        st.markdown("**Your story notes** (optional)")
        st.text_area("Your ideas", key=widget_key, placeholder="My idea is...", height=160,
                     on_change=keep_answer, label_visibility="collapsed")

    completed = sum(bool(value.strip()) for value in answers.values())
    st.caption(f"🌱 Ideas added to {completed} of 6 steps. All steps are optional.")
    left, right = st.columns(2, gap="small")
    with left:
        if st.button("← Back", use_container_width=True):
            keep_answer()
            if step > 0:
                st.session_state.planner_step -= 1
                st.rerun()
            go("prompt")
    with right:
        label = "Next step →" if step < 5 else "📖 Vocabulary →"
        if st.button(label, type="primary", use_container_width=True):
            keep_answer()
            if step < 5:
                st.session_state.planner_step += 1
                st.rerun()
            go("vocabulary")


def vocabulary():
    cat = st.session_state.selected["category"]
    st.markdown('<h1>📖 Vocabulary Treasure Box</h1>', unsafe_allow_html=True)
    st.markdown('<p class="intro">Prithvi, you already have a wonderful way with words! If you want inspiration, peek at these suggestions. Use any you like—or none at all.</p>', unsafe_allow_html=True)
    st.caption(f"50 words selected for your {cat.lower()} story")
    groups = vocabulary_for(cat)
    tabs = st.tabs(list(groups))
    for tab, (label, words) in zip(tabs, groups.items()):
        with tab:
            st.markdown('<div class="word-tags">' + ''.join(f'<span>{word}</span>' for word in words) + '</div>', unsafe_allow_html=True)
    st.markdown('<div class="quote">“Use any words you like—or none. Your own words matter most!”</div>', unsafe_allow_html=True)
    if st.button("🌟 I'm ready!", type="primary", use_container_width=True):
        go("good_luck")
    if st.button("← Back to planner", use_container_width=True):
        go("planner")


def good_luck():
    story = st.session_state.selected
    st.markdown('<h1>📖 My Story Plan</h1>', unsafe_allow_html=True)
    st.markdown(f"### ✨ {story['title']}")
    st.caption(f"{story['category']} · Keep this page open while you write in your notebook!")
    notes = st.session_state.get("plan_answers", {})
    for row_start in (0, 2, 4):
        cols = st.columns(2, gap="small")
        for offset, col in enumerate(cols):
            index = row_start + offset
            emoji, title, question = STEPS[index]
            with col:
                with st.container(border=True):
                    st.markdown(f"**{emoji} {index + 1}. {title}**")
                    st.write(question)
                    if notes.get(index, "").strip():
                        st.caption("💜 Your idea:")
                        st.write(notes[index])
                    else:
                        st.caption("You can think of an idea while writing. ✨")

    st.markdown('<div class="final-cheer"><strong>🌟 Good luck, Prithvi!</strong><div>Your imagination is amazing. Have fun writing your story—one sentence at a time! 💜</div></div>', unsafe_allow_html=True)

    if st.button("✏️ Change my plan", use_container_width=True):
        st.session_state.planner_step = 0
        go("planner")

    if st.button("🎡 Discover another story", type="primary", use_container_width=True):
        new_story()
        go("wheel")
    if st.button("🏠 Back to welcome", use_container_width=True):
        new_story()
        go("welcome")


def main():
    st.markdown(f"<style>{(BASE / 'assets/styles.css').read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
    for key, value in (('page', 'welcome'), ('spinning', False), ('selected', None), ('wheel_index', 0)):
        st.session_state.setdefault(key, value)
    story_pages = ('prompt', 'planner', 'vocabulary', 'good_luck')
    if st.session_state.page in story_pages and not st.session_state.selected:
        st.session_state.page = 'wheel'
    st.markdown('<div class="brand">✦ PRITHVI’S STORY WORLD ✦</div>', unsafe_allow_html=True)
    if st.session_state.page in ('wheel', *story_pages):
        st.caption('✨ Discover → 💡 Imagine → 📝 Plan → 📖 Explore words → 🌟 Good luck')
    {'welcome':welcome, 'wheel':wheel, 'prompt':prompt, 'planner':planner,
     'vocabulary':vocabulary, 'good_luck':good_luck, 'math_tables':math_tables,
     'math_quiz':math_quiz, 'math_results':math_results}[st.session_state.page]()


if __name__ == '__main__':
    main()

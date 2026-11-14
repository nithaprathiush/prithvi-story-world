# Prithvi's Story World — Complete Version 1

A personalized creative-writing companion built with Python and Streamlit.

## Features

- Time-aware greeting and custom kawaii portrait of Prithvi.
- Animated Spin / Stop wheel with ten story categories.
- 100 distinct story prompts, ten per category.
- Story premise and three imaginative hints.
- Landscape-first responsive layout for iPad 10th generation, also supporting portrait and laptop.
- Six-step planner showing one step at a time, large Back/Next controls, progress, and preserved optional idea fields.
- 50 topic-related vocabulary words organized into five compact tabs, without levels or examples.
- A final notebook-writing reference page showing the story title, all six planning questions, any notes entered, and a short Good Luck message.

No login, AI subscription, story writing editor, rewards, or database. Planning notes remain only during the Streamlit session.

## Run in Windows / VS Code

Requires Python 3.11+. Extract the ZIP, then open the `prithvi_story_world` folder in VS Code:

```powershell
py -3.11 -m venv .venv_prithvi
.\.venv_prithvi\Scripts\python.exe -m pip install -r requirements.txt
.\.venv_prithvi\Scripts\python.exe -m streamlit run app.py
```

You don't have to activate the virtual environment when invoking its Python executable directly.

Open `http://localhost:8501` if the browser doesn't open automatically.

## Customize

- Change `TIMEZONE = ZoneInfo("Asia/Kolkata")` in `app.py` if needed.
- Edit `assets/styles.css` for colors and spacing.
- Edit `data/story_data.py` for prompts, hints, and vocabulary.

## Host online

Upload the project files to GitHub and select `app.py` as the entry point in Streamlit Community Cloud. The illustration is bundled with the project and needs no outside image hosting.

# CS1970KF — Student Projects (Agentic Studio, Spring 2026)

This repository is a workspace of student sub-projects and exercises created for CSCI1970KF (Agentic Systems, Spring 2026). It is a collection of independent projects (each with its own entry point, tests, and data), not a single application.

## Quick links
- Course: https://cs.brown.edu/courses/csci1970kf/agentic-spr-2026/
- Assignments: https://cs.brown.edu/courses/csci1970kf/agentic-spr-2026/assignments.html
- Agent rules: `AGENTS.md`
- Repo internal doc: `REPO_DESCRIPTION.md`
- Testing plan: `TESTING.md`

## Top-level layout (very short descriptions)
- `airportweather-FrancisL0001/` — Airport Weather Analysis (Project 2): a Python program that produces charts showing relationships between weather metrics and daily flight delays using provided CSV datasets. Entry: `main.py`. Tests in `tests/`.
- `Project1/` — Project 1 (Setup + Stage 1): initial agentic-program setup and exercises (e.g., small intro-CS programs and research journal entries).
- `tetris-FrancisL0001/` — Tetris demos (Project 1 stages): browser-based Tetris implementations. Contains versions supporting dual gravity (“Tetris Dual Gravity”) and a test-focused stage (“Tetris Tested”) where logic is separated from UI for automated testing.
- `data-3-months/`, `data-5-days/` — Sample CSV datasets used by the airport weather project and its stages.
- `AGENTS.md` — Mandatory instructions for any automated agent or human collaborator.
- `TESTING.md` — Testing plan and testing strategy (per-course emphasis on tests).
- `REPO_DESCRIPTION.md` — (internal) detailed per-project descriptions and maintenance notes.

## Quick start — run tests (example)
- Using the included virtualenv for `airportweather` (if you want to reuse it):
```bash
# macOS / zsh
source airportweather-FrancisL0001/airport_weather_env/bin/activate
pytest -q
```
- Or create a fresh virtualenv and install required packages:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r airportweather-FrancisL0001/requirements.txt
pytest -q
```

- Deactivating the virtual environment once you are done:
```bash
deactivate # should work on most macOS and Bash systems
```

## How to run a sub-project (examples)
- Airport weather analysis:
```bash
cd airportweather-FrancisL0001
source airport_weather_env/bin/activate   # or use your venv
python main.py
```
- Tetris demo:
 - Open `tetris-FrancisL0001/index.html` in a browser.

## Contributing & agent rules
- Read `AGENTS.md` before making changes.
- Make minimal, scoped edits and explain non-trivial decisions.
- Don’t add dependencies silently — propose them and get approval.
- Tests should be added/updated in the project's `tests/` directory and follow `TESTING.md`.

## License
No license is included in the repo. Tell me your preferred license and I can add it.

## Contact
- Repo owner: FrancisL0001
- Course: CSCI1970KF, Spring 2026

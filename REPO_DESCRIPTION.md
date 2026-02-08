REPO DESCRIPTION — CS1970KF Projects (internal)

Purpose & vision
This repository collects independent course projects and exercises for CSCI1970KF (Agentic Systems, Spring 2026). Each subfolder is an independent project with its own entry point, data, and tests. This document is the canonical internal source-of-truth and should contain non-trivial decisions, assumptions, and maintenance guidance.

How to use this doc
- Keep this file updated when adding/removing sub-projects or changing major design/testing approaches.
- Use README for short, user-facing instructions; use this file for deeper notes.

Per-project detailed descriptions (based on course assignment pages)

1) airportweather-FrancisL0001 — Airport Weather Analysis (Project 2 / Part 1 & Part 2)
- Purpose: Produce graphs showing the relationship between weather conditions and flight delays (combine datasets from BTS and NOAA).
- What the assignment asks you to implement (high level, from course site):
  - A Python program that accepts an airport, date range, and a weather metric (precipitation, wind, visibility, or temperature) and produces a chart showing daily average flight delays overlaid with the chosen metric (Project 2 Part 1).
  - In Part 2, test the program on a larger `data-3-month` dataset and tighten testing and tests accordingly.
- Data files included:
  - `daily_flight_delays.csv`
  - `daily_weather.csv`
  - `airport_codes.csv`
  - (small sample sets in `data-5-days/`; larger set in `data-3-months/`)
- Entry points and structure:
  - `main.py` — runner that prompts/accepts inputs and generates charts.
  - `src/` — project modules (e.g., `data_loader.py`, `chart.py`, `ui.py`).
  - `tests/` — `pytest` tests for data loading, analysis, and chart outputs.
  - `requirements.txt` — packages used (pandas, matplotlib, pytest).
  - `airport_weather_env/` — committed virtualenv (present in repo); note: not portable across platforms; recommended to replace with `requirements.txt` + exclude venv from VCS in the future.
- Course expectations emphasized:
  - Provide `TESTING.md` describing testing strategy (why tests demonstrate trustworthiness).
  - Push Claude transcripts and journal entries as part of submission.
  - Use stepwise stages: Part 1 (5-day data) then Part 2 (3-month data).
- Maintenance notes:
  - If virtualenv removed, ensure `requirements.txt` fully reflects used packages.
  - Add a smoke test that runs `python main.py` on sample data to verify end-to-end behavior.

2) Project1 — Project 1 / Setup (Stage 1 and related early stages)
- Purpose: Dry run of the assignment workflow; write a first agentic program; set up a research journal.
- Course tasks distilled:
  - Copy the research journal template and name it `<lastname>-project1`.
  - Prompt Claude Code with: “write a program that belongs in an intro CS course” and save outputs; reflect in journal.
  - Commit work in stages and complete Canvas/Module surveys to unlock next stages.
- Structure in repo:
  - `Project1/` contains starter HTML files and small Python scripts (e.g., `guessing_game.py`).
  - Keep a short `TESTING.md` for this project when tests are added.
- Notes:
  - This project primarily documents the research journal and initial agentic interactions; code is intentionally simple.

3) tetris-FrancisL0001 — Tetris (Project 1 stages: Tetris Dual Gravity & Tetris Tested)
- Purpose: Iteratively develop a Tetris web app, explore agentic development, and add testing.
- Course-stage features and expectations:
  - Tetris Dual Gravity: add a mode toggle (press 'g') that switches between gravity down and anti-gravity (blocks rise up). Implemented as a web app (HTML/JS).
  - Tetris Tested: separate game logic from UI (move game model into JS module) and produce a testing plan; then create automated tests to validate core behaviors (piece movement, line clears, gravity behavior).
- Structure in repo:
  - `tetris-FrancisL0001/index.html`
  - `tetris-FrancisL0001/js/` — `game-controller.js`, `game-model.js`, `game-view.js`
  - Add `TESTING.md` describing what behaviors will be tested and why (per assignment).
- Notes:
  - For the "Tetris Tested" stage, include a testing plan first (prose), then automated tests (unit tests for the model).
  - Include a short description of how the work was tested (the assignment asks for a testing notes file).

Data & data-handling notes
- `data-5-days/` and `data-3-months/` mirror the course staging: smaller sample for Part 1, larger dataset for Part 2. Code should use relative paths (project root) to load data.
- Treat these CSVs as sample datasets; do not assume production-scale performance.

Testing strategy (repo-wide)
- Each project should include:
  - `TESTING.md` describing the strategy and key invariants.
  - Unit tests (pytest) that assert behavior (not implementation specifics).
  - Simple smoke tests that run main entrypoints using sample data.
- Suggested CI: add a small GitHub Actions workflow to run `pytest` on push/PR.

Assumptions & constraints
- Primary environment: macOS / Linux (zsh). Activation commands use `source`.
- Committed virtualenvs are present in some projects — not portable. Consider replacing them with `requirements.txt` entries and .gitignore updates (ask first).
- Python version compatibility: tests assume modern Python 3.8+ or 3.10+. Confirm with each project's `requirements.txt` or the virtualenv python binary.

Maintenance & recommended next steps
- Replace committed virtualenvs with `requirements.txt` and add `.gitignore` entries for venvs.
- Add a minimal CI workflow to run `pytest` automatically on push/PR.
- Add a `LICENSE` and optional `CONTRIBUTING.md`.
- Keep `REPO_DESCRIPTION.md` updated when adding/removing subprojects or changing testing or environment strategies.

References to course assignment pages used
- Project 1 (Setup / Stage 1): https://cs.brown.edu/courses/csci1970kf/agentic-spr-2026/assignments/Starter/setup.html
- Tetris Dual Gravity: https://cs.brown.edu/courses/csci1970kf/agentic-spr-2026/assignments/Starter/tetris-dual.html
- Tetris Tested: https://cs.brown.edu/courses/csci1970kf/agentic-spr-2026/assignments/Starter/tetris-tested.html
- Airport Weather (Part 1): https://cs.brown.edu/courses/csci1970kf/agentic-spr-2026/assignments/AirportWeather/version1.html
- Airport Weather (Part 2): https://cs.brown.edu/courses/csci1970kf/agentic-spr-2026/assignments/AirportWeather/version2.html

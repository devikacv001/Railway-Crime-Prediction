# Railway Crime Prediction GUI

Simple desktop GUI for predicting and visualizing railway-related arrests and a panic alert sender. Built with Python (Tkinter) and a small JavaScript/Node toolchain if present.

## Features
- Year-wise arrest prediction (calls `predict_arrests_for_year`).
- State-level trend plot (`plot_yearwise_rape_cases`).
- Total arrest trend plot (`plot_trend_2023_to_2030`).
- Panic/emergency alert via `panic_alert.py`.
- Windows-friendly setup and run instructions.

## Prerequisites
- Windows OS
- Python 3.8+ (download from `python.org`; includes `tkinter` by default)
- Optional: Node.js/npm if the repo contains `package.json`

## Project files (important)
- `main.py` — GUI entrypoint
- `prediction.py` — prediction and plotting logic
- `panic_alert.py` — emergency alert implementation (may need API keys/config)
- `predicted arrests/predicted_arrests_2030.csv` — states dataset used by the GUI
- `requirements.txt` — Python dependencies
- `git_push.ps1` — optional PowerShell helper to add/commit/pull/push

## Quick setup (Windows PowerShell)
1. Create and activate a venv:
   - `python -m venv .venv`
   - `.\.venv\Scripts\Activate.ps1`
2. Upgrade pip and install deps:
   - `pip install --upgrade pip`
   - If `requirements.txt` exists: `pip install -r requirements.txt`
   - Otherwise, common deps: `pip install pandas numpy matplotlib scikit-learn seaborn requests pillow`
3. Ensure the CSV data file is present at `predicted arrests/predicted_arrests_2030.csv`.
4. Place optional icons (`panic_icon.png`, `panic_icon2.png`) next to `main.py` or update paths.

## Run
- From the project root (venv activated):  
  `python main.py`

GUI default login credentials (for convenience/debugging):
- `admin` / `admin123`
- `1` / `1`

Change or remove these in `main.py` before production use.

## Panic alert configuration
Open `panic_alert.py` and configure any required API keys, phone numbers, or service endpoints. The GUI calls `send_emergency_alert()` without arguments; modify as needed.

## Notes
- Predictions and plotting functions are implemented in `prediction.py`. Running a prediction will attempt to save/plot output — check that file for where outputs are stored.
- If `tkinter` is missing, reinstall Python with Tcl/Tk support from `python.org`.

## Troubleshooting
- "CSV not found": confirm `predicted arrests/predicted_arrests_2030.csv` exists and path is correct.
- Icon load errors are non-fatal; GUI will run without icons.
- Rebase/push errors: use `git` to resolve conflicts manually. The provided `git_push.ps1` helps automate commit/pull/push on Windows.

## Contributing
- Fork the repo, create a branch, open a PR with description and tests if applicable.

## License
- Add a `LICENSE` file or update this README with the chosen license.

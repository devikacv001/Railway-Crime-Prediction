import os

# ─── Make sure our working directory is the project root ───────────────────
# This script lives in PROJECT_ROOT/Frontend/app.py,
# but your CSVs are in PROJECT_ROOT/*.csv
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)
# ────────────────────────────────────────────────────────────────────────────

from flask import Flask, render_template, request, jsonify
import pandas as pd

# then your other imports...
from prediction import predict_arrests_for_year
from panic_alert import send_emergency_alert

app = Flask(__name__)

# Preload the list of states for the dropdown
DF_STATES = pd.read_csv("predicted_arrests_2030.csv")
ALL_STATES = DF_STATES["State/UT"].dropna().tolist()

@app.route('/')
def index():
    return render_template('index.html', states=ALL_STATES)

@app.route('/predict', methods=['POST'])
def predict():
    payload = request.get_json()
    year = int(payload.get('year'))
    state = payload.get('state')
    predict_arrests_for_year(year)  # this writes predicted_arrests_{year}.csv
    dfp = pd.read_csv(f"predicted_arrests_{year}.csv")
    col = f"Predicted_Arrested_{year}"
    if state:
        val = int(dfp.loc[dfp["State/UT"] == state, col].values[0])
    else:
        val = int(dfp[col].sum())
    return jsonify({"year": year, "state": state or "ALL", "prediction": val})

@app.route('/panic', methods=['POST'])
def panic():
    try:
        send_emergency_alert()
        return jsonify({"status": "success", "message": "Emergency alert sent successfully!"}), 200
    except Exception as e:
        app.logger.error(f"Emergency alert error: {e}")
        return jsonify({"status": "error", "message": f"Failed to send emergency alert: {e}"}), 500

@app.route('/trend', methods=['POST'])
def trend():
    payload = request.get_json()
    state = payload.get('state')
    trend_data = {}
    for y in range(2023, 2031):
        dfp = pd.read_csv(f"predicted_arrests_{y}.csv")
        col = f"Predicted_Arrested_{y}"
        if state:
            trend_data[y] = int(dfp.loc[dfp["State/UT"] == state, col].values[0])
        else:
            trend_data[y] = int(dfp[col].sum())
    return jsonify({"state": state or "ALL", "trend": trend_data})

if __name__ == '__main__':
    app.run(debug=True)

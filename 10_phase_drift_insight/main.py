from models import PhaseState, Feedback

from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import csv
import os

app = FastAPI()

# CORSの許可設定（ブラウザUI連携用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 保存先ファイル
PHASE_JSON_FILE = "phase_state.json"
PHASE_CSV_FILE = "phase_state.csv"

# POST /phase_state
@app.post("/phase_state")
async def update_phase_state(phase_state: PhaseState = Body(...)):
    # JSONに保存
    with open(PHASE_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(phase_state.dict(), f, indent=4, ensure_ascii=False)

    # CSVに保存（ヘッダがなければ書く）
    file_exists = os.path.isfile(PHASE_CSV_FILE)
    with open(PHASE_CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["phase_name", "drift_value", "timestamp", "additional_info"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(phase_state.dict())

    return {"message": "Phase state updated successfully."}

# GET /current_phase
@app.get("/current_phase")
async def get_current_phase():
    if os.path.exists(PHASE_JSON_FILE):
        with open(PHASE_JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    else:
        return {"message": "No phase state available yet."}

# 簡単なHTMLビュー（ブラウザ確認用）
@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Phase Status</title>
    </head>
    <body>
        <h1>Current Phase Status</h1>
        <div id="phaseStatus">Loading...</div>

        <script>
            async function fetchPhaseStatus() {
                const response = await fetch('/current_phase');
                const data = await response.json();
                document.getElementById('phaseStatus').innerText = JSON.stringify(data, null, 2);
            }

            setInterval(fetchPhaseStatus, 2000);  // 2秒ごとに更新
            fetchPhaseStatus();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
# === フィードバック受信用 ===

# === フィードバックログ表示用HTML ===
@app.get("/feedback_status", response_class=HTMLResponse)
async def feedback_status_page():
    html_file_path = "feedback_status.html"
    if not os.path.exists(html_file_path):
        return HTMLResponse(content="Feedback status page not found.", status_code=404)
    
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    return HTMLResponse(content=html_content)

# === PhaseとFeedbackのダッシュボード用HTML ===
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page():
    html_file_path = "phase_feedback_dashboard.html"
    if not os.path.exists(html_file_path):
        return HTMLResponse(content="Dashboard page not found.", status_code=404)
    
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    return HTMLResponse(content=html_content)



# 保存先ファイル
FEEDBACK_CSV_FILE = "feedback_log.csv"

# POST /feedback
@app.post("/feedback")
async def submit_feedback(feedback: Feedback = Body(...)):
    file_exists = os.path.isfile(FEEDBACK_CSV_FILE)
    with open(FEEDBACK_CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["feedback_type", "details", "timestamp"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(feedback.dict())

    return {"message": "Feedback submitted successfully."}

# === フィードバック一覧取得用 ===

@app.get("/feedback_log")
async def get_feedback_log():
    if not os.path.exists(FEEDBACK_CSV_FILE):
        return {"message": "No feedback available yet."}

    feedback_list = []
    with open(FEEDBACK_CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            feedback_list.append(row)

    return feedback_list

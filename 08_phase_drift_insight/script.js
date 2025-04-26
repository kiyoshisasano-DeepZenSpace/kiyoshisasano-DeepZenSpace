async function fetchPhaseStatus() {
  const response = await fetch("/current_phase");
  const data = await response.json();
  const statusDiv = document.getElementById("phase-status");

  if (data.current_phase_state) {
    statusDiv.innerHTML = `<b>Current Phase:</b> ${data.current_phase_state.phase_state.current_phase}<br>
    <b>Drift Risk:</b> ${data.current_phase_state.phase_state.drift_risk}<br>
    <b>Latency Rhythm:</b> ${data.current_phase_state.phase_state.latency_rhythm}`;
  } else {
    statusDiv.innerHTML = "No Phase Data Available";
  }
}

async function fetchFeedbackLog() {
  const response = await fetch("/feedback_log");
  const data = await response.json();
  const logDiv = document.getElementById("feedback-log");
  logDiv.innerHTML = "";

  data.feedback_log.forEach(entry => {
    const div = document.createElement("div");
    div.className = "feedback-card";
    div.innerHTML = `<b>${entry.feedback_type}</b>: ${entry.details} (${entry.timestamp})`;
    logDiv.appendChild(div);
  });
}

async function sendFeedback(type) {
  const details = prompt(`Enter details for ${type}:`);
  if (details) {
    await fetch("/feedback", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ feedback_type: type, details: details })
    });
    fetchFeedbackLog();
  }
}

setInterval(fetchPhaseStatus, 2000);
setInterval(fetchFeedbackLog, 2000);

window.onload = () => {
  fetchPhaseStatus();
  fetchFeedbackLog();
};

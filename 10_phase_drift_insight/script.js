async function fetchPhaseState() {
    try {
      const res = await fetch("http://127.0.0.1:8000/current_phase");
      const data = await res.json();
      const state = data.current_phase_state;
  
      document.getElementById("phase").textContent = state.current_phase;
      document.getElementById("drift").textContent = state.drift_risk;
      document.getElementById("latency").textContent = state.latency;
    } catch (err) {
      console.error("Could not load phase state", err);
    }
  }
  
  // 初回実行＋10秒ごと更新
  fetchPhaseState();
  setInterval(fetchPhaseState, 10000);

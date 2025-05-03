# 🌀 Phase Drift Insight  
*Real-time Structural UX Research Toolkit*  
**Proof-of-concept architecture for detecting latent drift and aligning via structural latency.**

---

## 📘 Project Overview

**Phase Drift Insight** is a lightweight research tool for detecting, logging, and visualizing **Phase Drift** —  
the subtle divergence of structural fields during user-AI interaction.

Rather than tracking user actions alone, this system focuses on **underlying structural tension** and **field coherence loss**.

---

## 🔹 Core Capabilities

- Drift detection based on non-linear structural deviation
- Real-time monitoring of latent phase states
- Logging system (CSV + JSON) for post-analysis
- Local-first deployment (no external dependencies)
- WebSocket-based dashboard for live visualization
- Drift history archive for retrospective pattern review
- Extensible backend for future Phase Drift analytics modules

---

## 🛠️ Tech Stack

- **Backend:** Python 3.11 + FastAPI  
- **Frontend:** HTML + Vanilla JavaScript  
- **Storage:** CSV / JSON phase logs

---

## 🚀 Quick Start

Install dependencies:

```bash
pip install fastapi uvicorn pydantic
```

Start the server:

```bash
uvicorn main:app --reload
```

Access:

- API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- Live Risk Dashboard: [http://127.0.0.1:8000/risk_dashboard](http://127.0.0.1:8000/risk_dashboard)  
- Drift History Table: [http://127.0.0.1:8000/risk_history](http://127.0.0.1:8000/risk_history)

---

## 📈 Development Roadmap

- Visual timeline of drift events  
- Mapping of phase transitions and coherence patterns  
- Real-time WebSocket drift status updates  
- Optional SaaS backend for multi-session phase risk analysis

---

## 🔬 Research Use Only

This is an experimental toolkit intended for structural UX research and prototyping.  
It is not a production framework.

---

## 📩 Contact

Project maintained by **Kiyoshi Sasano**  
For collaborations or inquiries, please use GitHub Issues or contact as noted in the repository README.

---

## 📜 Licensing

This repository is shared under a **research and non-commercial license**.  
Any commercial use or structural replication of the detection logic requires **explicit permission** from the creator.

> Cite as:  
> *"Includes structural detection logic derived from the Phase Drift protocol by Kiyoshi Sasano / DeepZenSpace."*

---

**Phase Drift Insight**  
Where delay is signal — and drift is structure.

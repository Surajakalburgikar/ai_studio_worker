# AI Studio Worker 🚀

A modular, robust worker service for the AI Story Studio backend. The worker is responsible for fetching, processing, and completing jobs, handling cloud drive integration, and communicating with external AI providers.

---

## 📂 Project Structure

```text
AI_STUDIO_WORKER
│
├── worker/
│   ├── __init__.py
│   ├── main.py              # Main execution entrypoint
│   ├── config.py            # Configuration loader and schemas
│   │
│   ├── backend/             # Communication with main backend
│   │     ├── __init__.py
│   │     ├── client.py      # HTTP / WebSocket client
│   │     └── auth.py        # Authentication handlers
│   │
│   ├── queue/               # Queue polling and event ingestion
│   │     ├── __init__.py
│   │     └── poller.py      # Background queue poller
│   │
│   ├── models/              # Worker-side domain schemas
│   │     ├── __init__.py
│   │     ├── job.py         # Job payload schema
│   │     └── result.py      # Job completion result schema
│   │
│   ├── jobs/                # Job processing lifecycle
│   │     ├── __init__.py
│   │     ├── fetch.py       # Job ingestion from queue
│   │     ├── process.py     # Local orchestration & execution
│   │     └── complete.py    # Report status & results back
│   │
│   ├── image_providers/     # Execution runtimes / GPU runtimes for images
│   │     ├── __init__.py
│   │     ├── base.py        # Base provider interface
│   │     ├── mock.py        # Offline/Mock provider for testing
│   │     ├── colab.py       # Google Colab runner
│   │     └── kaggle.py      # Kaggle notebook runner
│   │
│   ├── storage/             # Abstract storage handlers (local, cloud, etc.)
│   │     ├── __init__.py
│   │     ├── base.py        # Storage backend base interface
│   │     ├── drive.py       # Google Drive storage backend
│   │     └── local.py       # Local disk storage backend
│   │
│   └── utils/               # Common shared helpers
│         └── __init__.py
│
├── generated/               # Directory for temporary run outputs (Git ignored)
├── logs/                    # Directory for log files (Git ignored)
├── .env                     # Local environment secrets (Git ignored)
├── requirements.txt         # Project dependencies
└── README.md                # Documentation


```

---

## 🛠️ Getting Started

### Prerequisites
* Python 3.10+
* Git

### Local Setup

1. **Clone the Repository:**
   ```powershell
   git clone https://github.com/Surajakalburgikar/ai_studio_worker.git
   cd ai_studio_worker
   ```

2. **Set up Virtual Environment:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configuration:**
   Copy configuration details to `.env` file (refer to `.env` template if variables are specified later).

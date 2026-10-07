# Cyber Defence System for Remote Professionals

An AI-driven, lightweight, and explainable cyber-risk assessment and defence-advisory platform designed specifically for remote employees, freelancers, independent contractors, and gig professionals who use personal devices, home networks, and public Wi-Fi without enterprise security infrastructure.

---

## 1. Project Overview & Problem Statement

Remote workers face hostile cyber threats (Wi-Fi eavesdropping, phishing credential harvesting, compromised endpoint devices, and account takeover) without the defensive telemetry and managed SOC services available in corporate enterprises. 

The **Cyber Defence System for Remote Professionals** bridges this gap by continuously evaluating non-invasive host telemetry, network posture, credential exposures, phishing risks, and login anomalies to produce an auditable **Cyber Risk Index (0–100)** with prioritized, human-readable remediation actions.

---

## 2. Core Architecture

```
USER INTERACTION (React + TypeScript + Tailwind CSS)
          │
          ▼
API GATEWAY & AUTHENTICATION (FastAPI + JWT + Bcrypt)
          │
          ▼
MASTER SECURITY ASSESSMENT PIPELINE
 ├── 1. Device Security Analyzer (Host Firewall, OS Updates, EDR Status)
 ├── 2. Network Security Analyzer (WPA2/WPA3 Ciphers, DNS Resolvers, Exposure Probes)
 ├── 3. Credential/Breach Intelligence Provider (HIBP API & Demo Corpus)
 ├── 4. AI/ML Module 1: Phishing URL Detector (Supervised Random Forest / Gradient Boosting)
 └── 5. AI/ML Module 2: Behavioural Anomaly Detector (Isolation Forest)
          │
          ▼
DETERMINISTIC NIST CSF RISK SCORING ENGINE
  Cyber Risk Index = (Device × 25%) + (Network × 20%) + (Credential × 20%) + (Phishing × 20%) + (Behaviour × 15%)
          │
          ▼
ACTIONABLE REMEDIATION RECOMMENDATION ENGINE (Ranked by Severity & Estimated Risk Reduction)
          │
          ▼
DATABASE PERSISTENCE (PostgreSQL / SQLite with SQLAlchemy & Audit Logging)
```

---

## 3. Technology Stack

- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS, Lucide React, Recharts, React Router v7, Axios.
- **Backend**: Python 3.13 / 3.11, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, Bcrypt, PyJWT.
- **Machine Learning**: scikit-learn (RandomForestClassifier, IsolationForest), pandas, numpy, joblib.
- **Database**: PostgreSQL (Production) / SQLite (Standalone Development & Testing).
- **Containerization**: Docker, Docker Compose.

---

## 4. Folder Structure

```
cyber-defence-system/
├── frontend/             # React + TypeScript + Vite frontend
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── pages/        # Dashboard, Device, Network, Phishing, Credentials, etc.
│   │   ├── layouts/      # MainLayout with sidebar & header
│   │   ├── services/     # Axios API service
│   │   ├── context/      # AuthContext
│   │   └── types/        # TypeScript interfaces
├── backend/              # FastAPI Application
│   └── app/
│       ├── api/          # REST route handlers
│       ├── core/         # Config, logging, settings
│       ├── models/       # SQLAlchemy models
│       ├── schemas/      # Pydantic schemas
│       ├── security/     # JWT authentication & bcrypt
│       ├── scanners/     # Device & Network safe telemetry scanners
│       ├── risk_engine/  # Deterministic NIST CSF scoring engine
│       ├── services/     # Master pipeline & Breach intelligence
│       └── recommendations/ # Prioritized remediation engine
├── ml/                   # Machine Learning Pipeline
│   ├── datasets/         # Benchmark dataset metadata
│   ├── preprocessing/    # Reproducible dataset preparation
│   ├── features/         # URL lexical & structural feature extractor
│   ├── training/         # Model training & comparative evaluation
│   ├── models/           # Serialized model artifacts (.joblib)
│   ├── evaluation/       # Benchmark metrics (accuracy, precision, recall, F1, ROC-AUC)
│   └── inference/        # PhishingPredictor & BehaviouralAnomalyDetector
├── tests/                # Automated pytest suite (Unit, ML, API, Integration)
├── scripts/              # Seed data script
├── docker/               # Dockerfiles for frontend and backend
├── docker-compose.yml    # Multi-container orchestration
├── .env.example          # Environment variables template
└── README.md
```

---

## 5. Risk Scoring Formula

The Cyber Risk Index (0–100) is calculated deterministically:

$$\text{Cyber Risk Index} = (D \times 0.25) + (N \times 0.20) + (C \times 0.20) + (P \times 0.20) + (B \times 0.15)$$

Where:
- **$D$ (Device Security)**: Host firewall, EDR status, patch compliance (25% weight).
- **$N$ (Network Security)**: Wi-Fi encryption, DNS leak indicators (20% weight).
- **$C$ (Credential Security)**: Known dark web breach exposure count (20% weight).
- **$P$ (Phishing Risk)**: Supervised ML probability score (20% weight).
- **$B$ (Behavioural Risk)**: Isolation Forest anomaly score (15% weight).

### Risk Bands:
- **0–24**: LOW RISK
- **25–49**: MODERATE RISK
- **50–74**: HIGH RISK
- **75–100**: CRITICAL RISK

---

## 6. Machine Learning Models & Datasets

### Supervised Phishing URL Classification
- **Datasets**: UCI Machine Learning Repository (Phishing Websites) + PhishTank verified corpus.
- **Extracted Features**: URL length, hostname length, entropy, subdomains, IP hostnames, @ symbol, suspicious tokens, shortening detection.
- **Model Benchmark**: Logistic Regression, Random Forest, Gradient Boosting.
- **Selected Model**: `RandomForestClassifier` / `LogisticRegression` ($F_1 \ge 0.95$).
- **Explainability**: Outputs specific detected indicators (e.g., Raw IP Hostname, Targeted Keyword Impersonation).

### Behavioural Anomaly Detection
- **Model**: `IsolationForest` ($n=100$, contamination=0.05).
- **Features**: Authentication hour, network context, geographical travel indicator, login burst frequency, session duration.

---

## 7. How to Run Locally

### Option A: Local Development

1. **Activate Backend**:
   ```bash
   cd cyber-defence-system
   # Set environment variable
   $env:PYTHONPATH="C:\Users\V\.gemini\antigravity-ide\scratch\cyber-defence-system;C:\Users\V\.gemini\antigravity-ide\scratch\cyber-defence-system\backend"
   
   # Run seed script
   python scripts/seed_data.py
   
   # Start FastAPI server
   uvicorn app.main:app --reload --port 8000
   ```

2. **Activate Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Open `http://localhost:5173` in your browser.

3. **Pre-seeded Academic Demo User**:
   - **Email**: `alex.freelancer@cyberwork.io`
   - **Password**: `CyberDefense2026!`

### Option B: Docker Compose

```bash
docker compose up --build
```
Access frontend at `http://localhost:5173` and backend at `http://localhost:8000/docs`.

---

## 8. Automated Testing

Run the full pytest suite:
```bash
pytest tests/
```
All 11 unit, integration, and ML tests validate scoring bounds, pipeline execution, token authentication, and model feature extraction.

---

## 9. Academic Disclaimer

This project is an AI-driven defensive cyber-risk prototype designed for educational demonstration and research. It does not provide infallible security guarantees and should be deployed in conjunction with standard zero-trust principles.

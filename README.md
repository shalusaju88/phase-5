# Project DEFI-FRAUD-053: Phase 5 Application Deployment
## Fairness-Constrained Ensemble Architectures for Latent Fraud Detection in Decentralized Finance Networks

**Target Publication:** IEEE Transactions on Information Forensics and Security (IEEE TIFS, 2026)  
**Authors:** Shalu C Saju & Yadhunandan TA  
**Affiliation:** Department of Cybersecurity, Srinivas University Institute of Engineering and Technology  

---

### Overview

Phase 5 delivers the production-ready microservice backend and institutional forensics dashboard for **Champion Model A**:
- **Stacking Meta-Classifier:** Tuned XGBoost, LightGBM, Random Forest, Extra Trees combined with regularized Logistic Regression ($C=2.0$).
- **Topological Manifold Representation:** Unsupervised Isolation Forest anomaly scoring + 3-Dimensional Riemannian UMAP embedding.
- **Lagrangian Algorithmic Fairness:** Demographic parity threshold calibration across wallet longevity tiers (ensuring Disparate Impact $\text{DI} \ge 0.80$, complying with legal standards).
- **Explainable AI (XAI):** High-fidelity Tree-SHAP attributions providing instance-level local forensic proofs and global macro-driver ranking.

---

### Architecture & File Structure

```
phase 5/
├── main.py              # FastAPI Production Microservice (REST API on port 8000)
├── app.py               # Gradio "Deep-Tech Noir" Forensic Web Dashboard (port 7860)
├── pipeline.py          # Core Inference Engine, Model A wrapper, & SHAP Renderer
├── requirements.txt     # Complete Python dependencies
├── test_phase5.py       # Automated End-to-End System Test Suite
├── README.md            # Deployment & Architectural Documentation
├── models/              # Serialized pipeline artifacts & cached weights
└── frontend/            # Modern React.js + Tailwind CSS "Deep-Tech Noir" Dashboard
    ├── package.json     # Node.js dependencies (React 18, Tailwind, Lucide, Axios)
    ├── vite.config.js   # Vite configuration with API proxy
    ├── tailwind.config.js # Deep-Tech Noir color palette & glow effects
    ├── index.html       # Web landing page
    ├── src/
    │   ├── App.jsx      # Main application container
    │   ├── main.jsx     # React root mount
    │   ├── index.css    # Tailwind directives & glassmorphism utilities
    │   ├── services/
    │   │   └── api.js   # Axios API client for FastAPI backend
    │   ├── data/
    │   │   └── presets.js # IEEE TIFS curated benchmark edge cases
    │   └── components/
    │       ├── Navbar.jsx
    │       ├── SingleTransactionForensics.jsx
    │       ├── BatchLedgerAudit.jsx
    │       ├── AblationMetrics.jsx
    │       ├── RiskGauge.jsx
    │       └── ShapWaterfallChart.jsx
    └── public/
        └── shield.svg   # Favicon
```

---

### Quick Start Instructions

#### 1. Launch FastAPI Backend (Terminal 1)
```bash
cd "phase 5"
pip install -r requirements.txt
python main.py
```
- **REST API URL:** `http://localhost:8000`
- **Interactive Swagger Docs:** `http://localhost:8000/docs`
- **Healthcheck:** `http://localhost:8000/healthcheck`

#### 2. Launch React.js Forensic Dashboard (Terminal 2)
```bash
cd "phase 5/frontend"
npm install
npm run dev
```
- **React Dashboard URL:** `http://localhost:5173`

---

### REST API Specification (`main.py`)

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Microservice catalog and active route overview. |
| `/healthcheck` | `GET` | Verifies microservice health, active pipeline components, and fairness calibration status. |
| `/predict` | `POST` | Primary inference endpoint for raw/unformatted single JSON transactions or batch arrays. Returns prediction flag, calibrated probability, risk tier, archetype, and local SHAP vector. |
| `/predict/csv` | `POST` | Upload multi-row CSV ledger dumps for batch forensic auditing. |
| `/model/metadata` | `GET` | Returns IEEE TIFS ablation study degradation metrics and Lagrangian fairness certificates. |
| `/examples/{case_id}`| `GET` | Returns curated benchmark edge cases (1: Stealth Sybil, 2: DEX LP, 3: Flash Arbitrage). |

---

### React.js Dashboard Features (`frontend/`)

1. **Tab 1: Single Transaction Forensics:**
   - Real-time parameter sliders & input controls categorized into Temporal, Ether Flow, ERC20 Routing, and Latent Manifolds.
   - 1-Click IEEE TIFS Curated Benchmark Preset loaders (Stealth Sybil, DEX Liquidity Provider, Flash Arbitrage Bot).
   - High-contrast verdict cards, confidence gauges, and Lagrangian fairness certificate.
   - Interactive **Tree-SHAP Waterfall attribution proof chart** showing exact positive (fraud escalators) and negative (benign anchors) log-odds shifts.
   - Behavioral Threat Archetype classification and mechanistic narrative.

2. **Tab 2: Batch Ledger Auditing:**
   - Drag-and-drop CSV ledger ingestion.
   - Real-time batch inference with high-throughput counter.
   - Searchable, filterable, and paginated forensic table with colored risk pills.
   - Export annotated audit report as CSV.

3. **Tab 3: IEEE TIFS 2026 Ablation Benchmark:**
   - 5-Model Tournament comparison matrix (Model A vs B vs C vs D vs E).
   - Detailed reviewer takeaways regarding latent manifolds and fairness constraints.

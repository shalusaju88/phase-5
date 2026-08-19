# Project DEFI-FRAUD-053: React.js Forensic Dashboard
## Deep-Tech Noir Web Dashboard for Decentralized Finance Fraud Forensics

This is the modern React.js + Tailwind CSS frontend for **Project DEFI-FRAUD-053** (*IEEE Transactions on Information Forensics and Security, 2026*).

---

### Features

1. **Tab 1: Single Transaction Forensics:**
   - Real-time transaction parameter sliders & input controls.
   - 1-Click IEEE TIFS Curated Benchmark Preset loaders (Stealth Sybil, DEX Liquidity Provider, Flash Arbitrage Bot).
   - High-contrast verdict cards, confidence gauges, and Lagrangian fairness certificate.
   - Dynamic **Tree-SHAP Waterfall attribution proof chart** showing exact positive (fraud escalators) and negative (benign anchors) log-odds shifts.
   - Behavioral Threat Archetype classification and mechanistic narrative.

2. **Tab 2: Batch Ledger Auditing:**
   - Drag-and-drop CSV ledger ingestion.
   - Real-time batch inference with high-throughput counter.
   - Searchable, filterable, and paginated forensic table with colored risk pills.
   - Export annotated audit report as CSV.

3. **Tab 3: IEEE TIFS 2026 Ablation Benchmark:**
   - 5-Model Tournament comparison matrix (Model A vs B vs C vs D vs E).
   - Demonstrates the empirical causal necessity of unsupervised latent manifolds and Lagrangian fairness calibration.

---

### Quick Start Instructions

#### 1. Start the FastAPI Backend (Terminal 1)
Make sure your Python virtual environment has the backend dependencies installed:
```bash
cd "phase 5"
python main.py
```
> FastAPI runs at: `http://localhost:8000` (Docs: `http://localhost:8000/docs`)

#### 2. Start the React Frontend (Terminal 2)
In a separate terminal window:
```bash
cd "phase 5/frontend"
npm install
npm run dev
```
> React Dashboard runs at: `http://localhost:5173`

---

### Environment Variables
By default, the frontend connects to `http://localhost:8000`. You can configure a custom backend URL by creating a `.env` file in the `frontend` folder:
```env
VITE_API_URL=http://localhost:8000
```

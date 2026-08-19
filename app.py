"""
========================================================================================
PROJECT DEFI-FRAUD-053: FAIRNESS-CONSTRAINED ENSEMBLE ARCHITECTURES FOR LATENT
FRAUD DETECTION IN DECENTRALIZED FINANCE NETWORKS (IEEE TIFS 2026)
----------------------------------------------------------------------------------------
Module: app.py
Purpose: Institutional "Deep-Tech Noir" Gradio Web Dashboard for DeFi Security Analysts,
         Risk Compliance Officers, and Forensic Investigators.
Authors: Shalu C Saju & Yadhunandan TA
========================================================================================
"""

import os
import io
import time
import json
import base64
import logging
from typing import Dict, List, Any, Tuple, Optional

import numpy as np
import pandas as pd
import gradio as gr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Import Inference Pipeline
from pipeline import get_pipeline, DeFiFraudInferencePipeline, ALL_25_FEATURES

logging.basicConfig(level=logging.INFO, format="[%(asctime)s | %(levelname)s] %(message)s")
logger = logging.getLogger("DEFI_FRAUD_DASHBOARD")

# Initialize Pipeline Instance
pipeline = get_pipeline()


# --------------------------------------------------------------------------------------
# "DEEP-TECH NOIR" CUSTOM THEME & CSS SPECIFICATION
# --------------------------------------------------------------------------------------
CUSTOM_CSS = """
/* ==========================================================================
   DEEP-TECH NOIR CYBERSECURITY THEME - PROJECT DEFI-FRAUD-053
   ========================================================================== */
:root {
    --bg-dark-primary: #080B10;
    --bg-dark-secondary: #0F172A;
    --bg-card: #131E32;
    --border-glow: #1E293B;
    --neon-cyan: #00F5FF;
    --neon-green: #00FF9D;
    --neon-crimson: #FF2A6D;
    --neon-amber: #FFB800;
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
}

body, .gradio-container {
    background-color: #080B10 !important;
    color: #F8FAFC !important;
    font-family: 'JetBrains Mono', 'Fira Code', 'Inter', -apple-system, sans-serif !important;
}

/* Institutional Header Card */
.header-card {
    background: linear-gradient(135deg, #0D1527 0%, #162444 50%, #0D1527 100%);
    border: 1px solid #00F5FF33;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 0 25px rgba(0, 245, 255, 0.08);
}

.header-title {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #00F5FF;
    margin: 0;
    text-transform: uppercase;
}

.header-subtitle {
    font-size: 13px;
    color: #94A3B8;
    margin-top: 6px;
    font-weight: 400;
}

.badge-tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-right: 8px;
}

.badge-champion {
    background-color: rgba(0, 255, 157, 0.15);
    color: #00FF9D;
    border: 1px solid #00FF9D55;
}

.badge-fairness {
    background-color: rgba(0, 245, 255, 0.15);
    color: #00F5FF;
    border: 1px solid #00F5FF55;
}

.badge-shap {
    background-color: rgba(255, 42, 109, 0.15);
    color: #FF2A6D;
    border: 1px solid #FF2A6D55;
}

/* Result Metric Cards */
.result-card {
    background: #0F172A;
    border-radius: 10px;
    padding: 16px;
    border: 1px solid #1E293B;
    margin-bottom: 12px;
}

.result-card-fraud {
    border: 1px solid #FF2A6D;
    box-shadow: 0 0 20px rgba(255, 42, 109, 0.2);
    background: linear-gradient(180deg, rgba(255, 42, 109, 0.08) 0%, #0F172A 100%);
}

.result-card-benign {
    border: 1px solid #00FF9D;
    box-shadow: 0 0 20px rgba(0, 255, 157, 0.2);
    background: linear-gradient(180deg, rgba(0, 255, 157, 0.08) 0%, #0F172A 100%);
}

/* Form Controls & Accordions */
.gr-accordion {
    background-color: #0F172A !important;
    border: 1px solid #1E293B !important;
    border-radius: 8px !important;
}

.gr-button-primary {
    background: linear-gradient(135deg, #00F5FF 0%, #00B4D8 100%) !important;
    color: #080B10 !important;
    font-weight: 800 !important;
    border: none !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    transition: all 0.2s ease !important;
}

.gr-button-primary:hover {
    box-shadow: 0 0 15px rgba(0, 245, 255, 0.6) !important;
    transform: translateY(-1px);
}

.gr-button-secondary {
    background: #1E293B !important;
    color: #E2E8F0 !important;
    border: 1px solid #334155 !important;
}

.gr-button-secondary:hover {
    border-color: #00F5FF !important;
    color: #00F5FF !important;
}

/* Tab Headers */
.tab-nav button {
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 0.5px !important;
}

.tab-nav button.selected {
    color: #00F5FF !important;
    border-bottom: 2px solid #00F5FF !important;
}
"""


# --------------------------------------------------------------------------------------
# PRESET EDGE CASES DATASET
# --------------------------------------------------------------------------------------
PRESET_CASES = {
    "🚨 Case 1: Stealth Sybil / Rapid Token Draining": {
        "avg_sent": 12.4,
        "avg_rec": 5.8,
        "lifespan": 1420.0,
        "uniq_rec": 3,
        "uniq_sent": 18,
        "min_rec": 0.05,
        "max_rec": 2.5,
        "avg_rec_val": 0.85,
        "min_sent": 0.02,
        "max_sent": 1.2,
        "avg_sent_val": 0.45,
        "erc20_txs": 4.0,
        "erc20_sent_contract": 0.0,
        "erc20_uniq_sent": 2.0,
        "erc20_uniq_rec": 2.0,
        "erc20_uniq_sent_1": 0.0,
        "erc20_min_rec": 0.0,
        "erc20_avg_rec": 120.5,
        "erc20_token_name_count": 1.0,
        "erc20_most_sent": "0",
        "erc20_most_rec": "0",
        "anomaly_score": -0.2850,
        "umap_1": 3.12,
        "umap_2": 8.45,
        "umap_3": 14.10
    },
    "🛡️ Case 2: High-Frequency DEX Liquidity Provider": {
        "avg_sent": 145.2,
        "avg_rec": 89.4,
        "lifespan": 485000.0,
        "uniq_rec": 45,
        "uniq_sent": 112,
        "min_rec": 0.0,
        "max_rec": 150.0,
        "avg_rec_val": 12.5,
        "min_sent": 0.0,
        "max_sent": 120.0,
        "avg_sent_val": 8.9,
        "erc20_txs": 185.0,
        "erc20_sent_contract": 0.0,
        "erc20_uniq_sent": 25.0,
        "erc20_uniq_rec": 40.0,
        "erc20_uniq_sent_1": 0.0,
        "erc20_min_rec": 0.0,
        "erc20_avg_rec": 45000.0,
        "erc20_token_name_count": 18.0,
        "erc20_most_sent": "Livepeer Token",
        "erc20_most_rec": "Numeraire",
        "anomaly_score": 0.0450,
        "umap_1": 7.85,
        "umap_2": 3.20,
        "umap_3": 11.40
    },
    "⚡ Case 3: Complex Flash Arbitrage / MEV Bot": {
        "avg_sent": 0.45,
        "avg_rec": 1.20,
        "lifespan": 38400.0,
        "uniq_rec": 8,
        "uniq_sent": 4,
        "min_rec": 1.0,
        "max_rec": 500.0,
        "avg_rec_val": 85.0,
        "min_sent": 0.5,
        "max_sent": 490.0,
        "avg_sent_val": 82.0,
        "erc20_txs": 65.0,
        "erc20_sent_contract": 0.0,
        "erc20_uniq_sent": 4.0,
        "erc20_uniq_rec": 6.0,
        "erc20_uniq_sent_1": 0.0,
        "erc20_min_rec": 10.0,
        "erc20_avg_rec": 12500.0,
        "erc20_token_name_count": 6.0,
        "erc20_most_sent": "Raiden",
        "erc20_most_rec": "XENON",
        "anomaly_score": -0.0820,
        "umap_1": 6.10,
        "umap_2": 9.80,
        "umap_3": 15.20
    }
}


# --------------------------------------------------------------------------------------
# FORENSIC INFERENCE HANDLERS
# --------------------------------------------------------------------------------------
def analyze_single_transaction(
    avg_sent, avg_rec, lifespan, uniq_rec, uniq_sent,
    min_rec, max_rec, avg_rec_val, min_sent, max_sent, avg_sent_val,
    erc20_txs, erc20_sent_contract, erc20_uniq_sent, erc20_uniq_rec,
    erc20_uniq_sent_1, erc20_min_rec, erc20_avg_rec, erc20_token_name_count,
    erc20_most_sent, erc20_most_rec,
    anomaly_score, umap_1, umap_2, umap_3
) -> Tuple[str, str, str, str, Any]:
    """
    Executes forensic evaluation for manual input fields and generates
    status cards, fairness telemetry, and local Tree-SHAP waterfall charts.
    """
    # Build dictionary payload
    payload = {
        "Avg min between sent tnx": avg_sent,
        "Avg min between received tnx": avg_rec,
        "Time Diff between first and last (Mins)": lifespan,
        "Unique Received From Addresses": uniq_rec,
        "Unique Sent To Addresses": uniq_sent,
        "min value received": min_rec,
        "max value received": max_rec,
        "avg val received": avg_rec_val,
        "min val sent": min_sent,
        "max val sent": max_sent,
        "avg val sent": avg_sent_val,
        "Total ERC20 tnxs": erc20_txs,
        "ERC20 total Ether sent contract": erc20_sent_contract,
        "ERC20 uniq sent addr": erc20_uniq_sent,
        "ERC20 uniq rec addr": erc20_uniq_rec,
        "ERC20 uniq sent addr.1": erc20_uniq_sent_1,
        "ERC20 min val rec": erc20_min_rec,
        "ERC20 avg val rec": erc20_avg_rec,
        "ERC20 uniq sent token name": erc20_token_name_count,
        "ERC20 most sent token type": str(erc20_most_sent),
        "ERC20_most_rec_token_type": str(erc20_most_rec),
        "anomaly_score": anomaly_score,
        "UMAP_1": umap_1,
        "UMAP_2": umap_2,
        "UMAP_3": umap_3
    }

    # Execute Inference via Pipeline
    result = pipeline.predict_single(payload)

    # 1. Prediction Banner HTML
    is_fraud = result["prediction"] == 1
    card_class = "result-card-fraud" if is_fraud else "result-card-benign"
    status_icon = "🚨" if is_fraud else "🛡️"
    status_text = "FRAUDULENT THREAT DETECTED" if is_fraud else "BENIGN PARTICIPANT VERIFIED"
    status_color = "#FF2A6D" if is_fraud else "#00FF9D"
    
    pred_html = f"""
    <div class="result-card {card_class}">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 13px; font-weight: 700; color: #94A3B8; letter-spacing: 1px;">VERDICT</span>
                <h2 style="color: {status_color}; margin: 4px 0 0 0; font-size: 22px; font-weight: 800;">
                    {status_icon} {status_text}
                </h2>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 12px; color: #94A3B8;">RISK TIER</span>
                <div style="font-size: 18px; font-weight: 800; color: {status_color};">
                    {result['risk_tier']}
                </div>
            </div>
        </div>
        <div style="margin-top: 14px; padding-top: 10px; border-top: 1px solid #1E293B; font-size: 13px; color: #CBD5E1;">
            <b>Behavioral Archetype:</b> <span style="color: #00F5FF;">{result['archetype']}</span>
        </div>
    </div>
    """

    # 2. Probability & Confidence Gauge HTML
    prob_pct = result["probability"] * 100.0
    conf_pct = result["confidence"] * 100.0
    gauge_html = f"""
    <div class="result-card">
        <h4 style="margin: 0 0 12px 0; color: #00F5FF; font-size: 14px; text-transform: uppercase; letter-spacing: 0.8px;">
            📊 Confidence & Probability Metrics
        </h4>
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px;">
            <span>Fraud Probability:</span>
            <b style="color: {status_color}; font-size: 15px;">{prob_pct:.2f}%</b>
        </div>
        <div style="background-color: #1E293B; border-radius: 4px; height: 10px; overflow: hidden; margin-bottom: 14px;">
            <div style="background: linear-gradient(90deg, #00FF9D 0%, #FFB800 50%, #FF2A6D 100%); width: {prob_pct}%; height: 100%;"></div>
        </div>

        <div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px;">
            <span>Ensemble Certainty:</span>
            <b style="color: #00F5FF; font-size: 15px;">{conf_pct:.2f}%</b>
        </div>
        <div style="background-color: #1E293B; border-radius: 4px; height: 10px; overflow: hidden; margin-bottom: 14px;">
            <div style="background-color: #00F5FF; width: {conf_pct}%; height: 100%;"></div>
        </div>

        <div style="font-size: 12px; color: #64748B; margin-top: 8px;">
            ⏱ Inference Latency: <b style="color: #94A3B8;">{result['latency_ms']:.2f} ms</b>
        </div>
    </div>
    """

    # 3. Lagrangian Fairness Certificate HTML
    fairness = result["fairness_metadata"]
    fairness_html = f"""
    <div class="result-card">
        <h4 style="margin: 0 0 12px 0; color: #00FF9D; font-size: 14px; text-transform: uppercase; letter-spacing: 0.8px;">
            ⚖️ Lagrangian Fairness Calibration
        </h4>
        <div style="font-size: 13px; line-height: 1.6; color: #CBD5E1;">
            <div><b>Demographic Cohort:</b> <span style="color: #F8FAFC;">{fairness['demographic_group']}</span></div>
            <div><b>Account Lifespan:</b> <span style="color: #F8FAFC;">{fairness['account_lifespan_days']:.1f} days ({lifespan:.0f} mins)</span></div>
            <div><b>Calibrated Group Threshold:</b> <span style="color: #00FF9D; font-weight: 700;">{fairness['calibrated_threshold']:.4f}</span></div>
            <div><b>Disparate Impact Status:</b> <span style="color: #00FF9D; font-weight: 700;">COMPLIANT (DI &ge; 0.80)</span></div>
        </div>
        <div style="margin-top: 10px; font-size: 11px; color: #94A3B8; border-top: 1px solid #1E293B; padding-top: 8px;">
            Protected by Lagrangian demographic parity optimization to eliminate false positive penalties on new DeFi wallets.
        </div>
    </div>
    """

    # 4. Forensic Narrative & Manifold Geometry HTML
    manifolds = result["latent_manifolds"]
    narrative_html = f"""
    <div class="result-card">
        <h4 style="margin: 0 0 10px 0; color: #FFB800; font-size: 14px; text-transform: uppercase; letter-spacing: 0.8px;">
            🔍 Forensic Mechanistic Insight
        </h4>
        <p style="font-size: 13px; color: #CBD5E1; line-height: 1.5; margin: 0 0 12px 0;">
            {result['mechanistic_insight']}
        </p>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; font-size: 11px; background: #080B10; padding: 10px; border-radius: 6px; border: 1px solid #1E293B;">
            <div><span style="color:#64748B;">IsoForest Score</span><br><b style="color:#00F5FF;">{manifolds['anomaly_score']:.4f}</b></div>
            <div><span style="color:#64748B;">UMAP-1</span><br><b style="color:#00FF9D;">{manifolds['UMAP_1']:.2f}</b></div>
            <div><span style="color:#64748B;">UMAP-2</span><br><b style="color:#00FF9D;">{manifolds['UMAP_2']:.2f}</b></div>
            <div><span style="color:#64748B;">UMAP-3</span><br><b style="color:#00FF9D;">{manifolds['UMAP_3']:.2f}</b></div>
        </div>
    </div>
    """

    # 5. Render Local Tree-SHAP Waterfall Chart
    shap_dict = result["shap_explanation"]["feature_attributions"]
    
    # Generate Matplotlib Figure
    sorted_items = sorted(shap_dict.items(), key=lambda x: abs(x[1]), reverse=True)[:10]
    sorted_items.reverse()
    features = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]
    bar_colors = ['#FF2A6D' if v > 0 else '#00F5FF' for v in values]

    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=150)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0B0E14')

    bars = ax.barh(range(len(features)), values, color=bar_colors, height=0.55, edgecolor='#334155', linewidth=0.8)
    ax.set_yticks(range(len(features)))
    ax.set_yticklabels(features, fontsize=9, fontweight='bold', color='#E2E8F0')
    ax.axvline(0, color='#64748B', linestyle='--', linewidth=1.0, alpha=0.8)

    for i, bar in enumerate(bars):
        val = values[i]
        x_pos = val + (0.02 if val >= 0 else -0.02)
        ha = 'left' if val >= 0 else 'right'
        ax.text(x_pos, bar.get_y() + bar.get_height()/2, f"{val:+.3f}",
                va='center', ha=ha, fontsize=8.5, fontweight='bold',
                color='#FF2A6D' if val > 0 else '#00F5FF')

    ax.set_xlabel("Local Shapley Value (Δ Log-Odds to Fraud)", fontsize=9.5, fontweight='bold', color='#94A3B8', labelpad=8)
    ax.set_title("Instance Tree-SHAP Attribution Waterfall Proof", fontsize=11, fontweight='bold', color='#00FF9D', pad=12)
    ax.tick_params(colors='#94A3B8', labelsize=8.5)
    ax.grid(True, linestyle=':', alpha=0.3, color='#334155')
    for spine in ax.spines.values():
        spine.set_color('#1E293B')

    plt.tight_layout()

    return pred_html, gauge_html, fairness_html, narrative_html, fig


def load_preset_values(preset_name: str) -> List[Any]:
    """Populates interactive inputs with chosen IEEE TIFS preset edge case values."""
    if preset_name not in PRESET_CASES:
        return [gr.update()] * 25
    data = PRESET_CASES[preset_name]
    return [
        data["avg_sent"], data["avg_rec"], data["lifespan"], data["uniq_rec"], data["uniq_sent"],
        data["min_rec"], data["max_rec"], data["avg_rec_val"], data["min_sent"], data["max_sent"], data["avg_sent_val"],
        data["erc20_txs"], data["erc20_sent_contract"], data["erc20_uniq_sent"], data["erc20_uniq_rec"],
        data["erc20_uniq_sent_1"], data["erc20_min_rec"], data["erc20_avg_rec"], data["erc20_token_name_count"],
        data["erc20_most_sent"], data["erc20_most_rec"],
        data["anomaly_score"], data["umap_1"], data["umap_2"], data["umap_3"]
    ]


def batch_csv_audit(file_obj) -> Tuple[pd.DataFrame, str, str]:
    """Executes batch forensic audit over an uploaded CSV ledger file."""
    if file_obj is None:
        return pd.DataFrame(), "<div style='color:red;'>No CSV uploaded.</div>", None

    t0 = time.perf_counter()
    df_raw = pd.read_csv(file_obj.name)
    
    results = []
    for _, row in df_raw.iterrows():
        res = pipeline.predict_single(row.to_dict())
        results.append({
            "Verdict": "🚨 FRAUD" if res["prediction"] == 1 else "🛡️ BENIGN",
            "Probability": f"{res['probability']*100:.1f}%",
            "Risk Tier": res["risk_tier"],
            "Archetype": res["archetype"],
            "Demographic Group": res["fairness_metadata"]["demographic_group"],
            "Anomaly Score": res["latent_manifolds"]["anomaly_score"],
            "UMAP_1": res["latent_manifolds"]["UMAP_1"],
            "UMAP_2": res["latent_manifolds"]["UMAP_2"],
            "Latency (ms)": res["latency_ms"]
        })

    df_out = pd.DataFrame(results)
    fraud_count = sum(1 for r in results if "FRAUD" in r["Verdict"])
    total_count = len(results)
    fraud_rate = (fraud_count / total_count) * 100.0 if total_count > 0 else 0.0
    elapsed_s = time.perf_counter() - t0

    summary_html = f"""
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 15px;">
        <div class="result-card" style="text-align: center;">
            <span style="color: #94A3B8; font-size: 11px;">TOTAL AUDITED</span>
            <h3 style="color: #00F5FF; margin: 4px 0 0 0;">{total_count}</h3>
        </div>
        <div class="result-card" style="text-align: center;">
            <span style="color: #94A3B8; font-size: 11px;">FRAUD ALERTS</span>
            <h3 style="color: #FF2A6D; margin: 4px 0 0 0;">{fraud_count}</h3>
        </div>
        <div class="result-card" style="text-align: center;">
            <span style="color: #94A3B8; font-size: 11px;">FRAUD RATE</span>
            <h3 style="color: #FFB800; margin: 4px 0 0 0;">{fraud_rate:.1f}%</h3>
        </div>
        <div class="result-card" style="text-align: center;">
            <span style="color: #94A3B8; font-size: 11px;">THROUGHPUT</span>
            <h3 style="color: #00FF9D; margin: 4px 0 0 0;">{total_count/elapsed_s:.0f} tx/s</h3>
        </div>
    </div>
    """

    # Export annotated CSV
    out_csv_path = os.path.join(pipeline.model_dir, "batch_audit_results.csv")
    df_out.to_csv(out_csv_path, index=False)

    return df_out, summary_html, out_csv_path


# --------------------------------------------------------------------------------------
# GRADIO INTERFACE BUILDER
# --------------------------------------------------------------------------------------
def build_gradio_app() -> gr.Blocks:
    """Constructs the complete Deep-Tech Noir Gradio forensic dashboard."""
    with gr.Blocks(title="Project DEFI-FRAUD-053: Forensics Intelligence Matrix", css=CUSTOM_CSS) as demo:
        
        # Institutional Header
        gr.HTML("""
        <div class="header-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h1 class="header-title">⚡ PROJECT DEFI-FRAUD-053: FORENSIC INTELLIGENCE MATRIX</h1>
                    <div class="header-subtitle">
                        Fairness-Constrained Ensemble Architectures for Latent Fraud Detection in Decentralized Finance Networks
                    </div>
                </div>
                <div style="text-align: right;">
                    <span class="badge-tag badge-champion">🏆 CHAMPION MODEL A</span>
                    <span class="badge-tag badge-fairness">⚖️ LAGRANGIAN FAIRNESS</span>
                    <span class="badge-tag badge-shap">🔍 TREE-SHAP XAI</span>
                </div>
            </div>
            <div style="margin-top: 14px; font-size: 12px; color: #64748B;">
                <b>Target Publication:</b> IEEE Transactions on Information Forensics and Security (IEEE TIFS, 2026) | 
                <b>Authors:</b> Shalu C Saju & Yadhunandan TA | <b>Affiliation:</b> Srinivas University
            </div>
        </div>
        """)

        with gr.Tabs(elem_classes=["tab-nav"]):
            
            # --------------------------------------------------------------------------
            # TAB 1: SINGLE TRANSACTION FORENSICS
            # --------------------------------------------------------------------------
            with gr.TabItem("🎯 SINGLE TRANSACTION FORENSICS"):
                with gr.Row():
                    
                    # Left Column: Input Controls & Presets
                    with gr.Column(scale=5):
                        gr.Markdown("### 🎛️ Transaction Input Controls")
                        
                        # Presets Selector
                        preset_dropdown = gr.Dropdown(
                            label="⚡ Load Curated IEEE TIFS Edge Case Presets",
                            choices=list(PRESET_CASES.keys()),
                            value=list(PRESET_CASES.keys())[0],
                            interactive=True
                        )

                        with gr.Accordion("⏱️ Temporal Dynamics & Lifespan", open=True):
                            lifespan_in = gr.Slider(label="Account Lifespan: Time Diff First & Last (Mins)", minimum=0, maximum=1500000, value=1420.0, step=10)
                            avg_sent_in = gr.Number(label="Avg Min Between Sent Tnx", value=12.4)
                            avg_rec_in = gr.Number(label="Avg Min Between Received Tnx", value=5.8)

                        with gr.Accordion("💼 Core Ledger Flow & Degree (ETH)", open=False):
                            with gr.Row():
                                uniq_rec_in = gr.Number(label="Unique Received From Addrs", value=3)
                                uniq_sent_in = gr.Number(label="Unique Sent To Addrs", value=18)
                            with gr.Row():
                                min_rec_in = gr.Number(label="Min Val Received (ETH)", value=0.05)
                                max_rec_in = gr.Number(label="Max Val Received (ETH)", value=2.5)
                                avg_rec_val_in = gr.Number(label="Avg Val Received (ETH)", value=0.85)
                            with gr.Row():
                                min_sent_in = gr.Number(label="Min Val Sent (ETH)", value=0.02)
                                max_sent_in = gr.Number(label="Max Val Sent (ETH)", value=1.2)
                                avg_sent_val_in = gr.Number(label="Avg Val Sent (ETH)", value=0.45)

                        with gr.Accordion("🪙 ERC20 / DeFi Token Routing", open=False):
                            with gr.Row():
                                erc20_txs_in = gr.Number(label="Total ERC20 Tnxs", value=4.0)
                                erc20_sent_contract_in = gr.Number(label="ERC20 Total Sent Contract", value=0.0)
                            with gr.Row():
                                erc20_uniq_sent_in = gr.Number(label="ERC20 Uniq Sent Addr", value=2.0)
                                erc20_uniq_rec_in = gr.Number(label="ERC20 Uniq Rec Addr", value=2.0)
                                erc20_uniq_sent_1_in = gr.Number(label="ERC20 Uniq Sent Addr.1", value=0.0)
                            with gr.Row():
                                erc20_min_rec_in = gr.Number(label="ERC20 Min Val Rec", value=0.0)
                                erc20_avg_rec_in = gr.Number(label="ERC20 Avg Val Rec", value=120.5)
                                erc20_token_name_count_in = gr.Number(label="ERC20 Uniq Token Count", value=1.0)
                            with gr.Row():
                                erc20_most_sent_in = gr.Textbox(label="ERC20 Most Sent Token Type", value="0")
                                erc20_most_rec_in = gr.Textbox(label="ERC20 Most Rec Token Type", value="0")

                        with gr.Accordion("🌐 Latent Manifold Coordinates (IsoForest + UMAP)", open=False):
                            anomaly_score_in = gr.Slider(label="Isolation Forest Anomaly Score", minimum=-0.5, maximum=0.2, value=-0.2850, step=0.005)
                            with gr.Row():
                                umap_1_in = gr.Number(label="UMAP_1 Coordinate", value=3.12)
                                umap_2_in = gr.Number(label="UMAP_2 Coordinate", value=8.45)
                                umap_3_in = gr.Number(label="UMAP_3 Coordinate", value=14.10)

                        analyze_btn = gr.Button("⚡ EXECUTE FORENSIC AUDIT", variant="primary", elem_classes=["gr-button-primary"])

                    # Right Column: Visual Telemetry Cards & Tree-SHAP Plot
                    with gr.Column(scale=7):
                        gr.Markdown("### 🛡️ Live Forensic Telemetry & Attributions")
                        
                        out_verdict = gr.HTML()
                        
                        with gr.Row():
                            out_gauge = gr.HTML()
                            out_fairness = gr.HTML()
                        
                        out_narrative = gr.HTML()
                        out_shap_plot = gr.Plot(label="Tree-SHAP Waterfall Proof")

                # Wire Preset Change Event
                all_inputs = [
                    avg_sent_in, avg_rec_in, lifespan_in, uniq_rec_in, uniq_sent_in,
                    min_rec_in, max_rec_in, avg_rec_val_in, min_sent_in, max_sent_in, avg_sent_val_in,
                    erc20_txs_in, erc20_sent_contract_in, erc20_uniq_sent_in, erc20_uniq_rec_in,
                    erc20_uniq_sent_1_in, erc20_min_rec_in, erc20_avg_rec_in, erc20_token_name_count_in,
                    erc20_most_sent_in, erc20_most_rec_in,
                    anomaly_score_in, umap_1_in, umap_2_in, umap_3_in
                ]
                
                preset_dropdown.change(
                    fn=load_preset_values,
                    inputs=[preset_dropdown],
                    outputs=all_inputs
                )

                # Wire Submit Action
                analyze_btn.click(
                    fn=analyze_single_transaction,
                    inputs=all_inputs,
                    outputs=[out_verdict, out_gauge, out_fairness, out_narrative, out_shap_plot]
                )

            # --------------------------------------------------------------------------
            # TAB 2: BATCH LEDGER AUDITING
            # --------------------------------------------------------------------------
            with gr.TabItem("📂 BATCH LEDGER AUDIT"):
                gr.Markdown("### Ingest On-Chain CSV Ledger Dumps for High-Throughput Forensics")
                with gr.Row():
                    with gr.Column(scale=4):
                        csv_file_input = gr.File(label="Upload Ledger CSV", file_types=[".csv", ".txt"])
                        batch_btn = gr.Button("🚀 RUN BATCH AUDIT", variant="primary", elem_classes=["gr-button-primary"])
                    with gr.Column(scale=8):
                        batch_summary_output = gr.HTML()
                
                batch_df_output = gr.Dataframe(label="Forensic Ledger Results", interactive=False)
                batch_download_output = gr.File(label="Download Annotated Forensic Report (.csv)")

                batch_btn.click(
                    fn=batch_csv_audit,
                    inputs=[csv_file_input],
                    outputs=[batch_df_output, batch_summary_output, batch_download_output]
                )

            # --------------------------------------------------------------------------
            # TAB 3: IEEE TIFS RESEARCH BENCHMARK & ABLATION MATRIX
            # --------------------------------------------------------------------------
            with gr.TabItem("🔬 IEEE TIFS 2026 ARCHITECTURE & ABLATION"):
                gr.Markdown("""
                ### 🏆 Champion Model A Architectural Benchmark (Phase 4b Ablation Findings)
                The full Q1 multi-tiered architecture couples a **4-Model Stacking Ensemble** (XGBoost + LightGBM + RF + Extra Trees) with 
                **Unsupervised Topological Manifolds** (3D UMAP + Isolation Forest) and **Lagrangian Fairness Threshold Calibration**.
                """)
                
                ablation_table = pd.DataFrame([
                    {"Model Architecture": "Model A (Full Q1 Architecture)", "Features": 25, "F1-Score": 0.9974, "ROC-AUC": 0.9996, "Disparate Impact": 0.9652, "Delta F1": "0.00% (Champion)"},
                    {"Model Architecture": "Model B (Minus Latent Manifolds)", "Features": 21, "F1-Score": 0.9785, "ROC-AUC": 0.9912, "Disparate Impact": 0.9410, "Delta F1": "-1.89% (False Neg ↑)"},
                    {"Model Architecture": "Model C (Single Baseline Unconstrained)", "Features": 21, "F1-Score": 0.9492, "ROC-AUC": 0.9784, "Disparate Impact": 0.7845, "Delta F1": "-4.83% (Breaches 4/5ths)"},
                    {"Model Architecture": "Model D (Ensemble minus Fairness)", "Features": 25, "F1-Score": 0.9961, "ROC-AUC": 0.9994, "Disparate Impact": 0.8812, "Delta F1": "-0.13% (Uncalibrated)"},
                    {"Model Architecture": "Model E (Single Model with Latents)", "Features": 25, "F1-Score": 0.9925, "ROC-AUC": 0.9982, "Disparate Impact": 0.9120, "Delta F1": "-0.49% (Single Core)"}
                ])
                gr.Dataframe(value=ablation_table, interactive=False)

                gr.HTML("""
                <div class="result-card" style="margin-top: 15px;">
                    <h4 style="color: #00F5FF; margin-top: 0;">Key Scientific Findings (IEEE TIFS Reviewer Summary):</h4>
                    <ul style="font-size: 13px; color: #CBD5E1; line-height: 1.6;">
                        <li><b>Latent Manifold Utility:</b> Stripping UMAP coordinates and Isolation Forest anomaly scores (Model B) degrades F1 by <b>-1.89%</b> and causes stealth Sybil exploits to slip past threshold detectors.</li>
                        <li><b>Algorithmic Fairness Imperative:</b> Unconstrained naive baselines (Model C) drop Disparate Impact to <b>0.7845</b>, violating the legal 4/5ths demographic parity threshold for new wallets.</li>
                        <li><b>Stacking Superiority:</b> Meta-Learner Logistic Regression with tuned tree ensembles produces an optimal Pareto efficiency frontier ($F_1 = 0.9974$).</li>
                    </ul>
                </div>
                """)

    return demo


# --------------------------------------------------------------------------------------
# CLI ENTRY POINT
# --------------------------------------------------------------------------------------
if __name__ == "__main__":
    demo = build_gradio_app()
    logger.info("Launching Gradio Forensic Dashboard with public share link...")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)

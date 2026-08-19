"""
========================================================================================
PROJECT DEFI-FRAUD-053: FAIRNESS-CONSTRAINED ENSEMBLE ARCHITECTURES FOR LATENT
FRAUD DETECTION IN DECENTRALIZED FINANCE NETWORKS (IEEE TIFS 2026)
----------------------------------------------------------------------------------------
Module: main.py
Purpose: Production-grade FastAPI Microservice for DeFi Fraud Inference,
         Topological Manifold Extraction, Lagrangian Fairness Calibration,
         and Tree-SHAP Local Explainability.
Authors: Shalu C Saju & Yadhunandan TA
========================================================================================
"""

import os
import io
import time
import json
import logging
from typing import Dict, List, Any, Optional, Union
from contextlib import asynccontextmanager

import numpy as np
import pandas as pd
from fastapi import FastAPI, Request, HTTPException, status, UploadFile, File, Query, Path
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict

# Import Core Pipeline Engine
from pipeline import get_pipeline, DeFiFraudInferencePipeline, ALL_25_FEATURES, RAW_LEDGER_FEATURES

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s | %(levelname)s | %(name)s] %(message)s"
)
logger = logging.getLogger("DEFI_FRAUD_API")


# --------------------------------------------------------------------------------------
# PYDANTIC INPUT & OUTPUT SCHEMAS (DEFENSE-GRADE VALIDATION)
# --------------------------------------------------------------------------------------
class RawTransactionPayload(BaseModel):
    """
    Validation schema for raw on-chain Ethereum / DeFi ledger transaction attributes.
    All fields are optional with intelligent fallback defaults to support unformatted inputs.
    """
    model_config = ConfigDict(extra='allow', populate_by_name=True)

    # Core Temporal Dynamics
    avg_min_between_sent_tnx: Optional[float] = Field(
        default=0.0,
        alias="Avg min between sent tnx",
        description="Average time in minutes between outbound transactions sent by this account."
    )
    avg_min_between_received_tnx: Optional[float] = Field(
        default=0.0,
        alias="Avg min between received tnx",
        description="Average time in minutes between inbound transactions received by this account."
    )
    time_diff_between_first_and_last_mins: Optional[float] = Field(
        default=1000.0,
        alias="Time Diff between first and last (Mins)",
        description="Total active lifespan of the account on-chain in minutes (Sensitive attribute for fairness)."
    )

    # Address Diversity & Degree Metrics
    unique_received_from_addresses: Optional[float] = Field(
        default=1.0,
        alias="Unique Received From Addresses",
        description="Number of distinct counterparties sending assets to this address."
    )
    unique_sent_to_addresses: Optional[float] = Field(
        default=1.0,
        alias="Unique Sent To Addresses",
        description="Number of distinct recipient counterparties."
    )

    # Native Ether Value Metrics
    min_value_received: Optional[float] = Field(default=0.0, alias="min value received")
    max_value_received: Optional[float] = Field(default=0.0, alias="max value received")
    avg_val_received: Optional[float] = Field(default=0.0, alias="avg val received")
    min_val_sent: Optional[float] = Field(default=0.0, alias="min val sent")
    max_val_sent: Optional[float] = Field(default=0.0, alias="max val sent")
    avg_val_sent: Optional[float] = Field(default=0.0, alias="avg val sent")

    # ERC20 / DeFi Protocol Features
    total_erc20_tnxs: Optional[float] = Field(default=0.0, alias="Total ERC20 tnxs")
    erc20_total_ether_sent_contract: Optional[float] = Field(default=0.0, alias="ERC20 total Ether sent contract")
    erc20_uniq_sent_addr: Optional[float] = Field(default=0.0, alias="ERC20 uniq sent addr")
    erc20_uniq_rec_addr: Optional[float] = Field(default=0.0, alias="ERC20 uniq rec addr")
    erc20_uniq_sent_addr_1: Optional[float] = Field(default=0.0, alias="ERC20 uniq sent addr.1")
    erc20_min_val_rec: Optional[float] = Field(default=0.0, alias="ERC20 min val rec")
    erc20_avg_val_rec: Optional[float] = Field(default=0.0, alias="ERC20 avg val rec")
    erc20_uniq_sent_token_name: Optional[float] = Field(default=0.0, alias="ERC20 uniq sent token name")
    erc20_most_sent_token_type: Optional[Union[str, int, float]] = Field(default="0", alias="ERC20 most sent token type")
    erc20_most_rec_token_type: Optional[Union[str, int, float]] = Field(default="0", alias="ERC20_most_rec_token_type")

    # Optional Pre-computed Manifold Features (Calculated automatically if omitted)
    anomaly_score: Optional[float] = Field(default=None, alias="anomaly_score")
    umap_1: Optional[float] = Field(default=None, alias="UMAP_1")
    umap_2: Optional[float] = Field(default=None, alias="UMAP_2")
    umap_3: Optional[float] = Field(default=None, alias="UMAP_3")


class BatchTransactionPayload(BaseModel):
    """Batch container for multi-transaction audits."""
    transactions: List[RawTransactionPayload]


class LatentManifoldsResponse(BaseModel):
    anomaly_score: float
    UMAP_1: float
    UMAP_2: float
    UMAP_3: float


class FairnessMetadataResponse(BaseModel):
    sensitive_attribute: str
    demographic_group: str
    account_lifespan_days: float
    calibrated_threshold: float
    disparate_impact_compliant: bool


class ShapDriverItem(BaseModel):
    feature: str
    shap_value: float
    impact: str


class ShapExplanationResponse(BaseModel):
    base_value: float
    feature_attributions: Dict[str, float]
    top_risk_drivers: List[ShapDriverItem]
    top_mitigating_factors: List[ShapDriverItem]


class SinglePredictionResponse(BaseModel):
    """Comprehensive forensic intelligence response schema."""
    prediction: int = Field(description="Fraud flag: 0 (Benign) or 1 (Fraud)")
    fraud_status: str = Field(description="FRAUD_ALERT or BENIGN_VERIFIED")
    probability: float = Field(description="Calibrated probability of fraudulent activity [0.0 - 1.0]")
    confidence: float = Field(description="Certainty score [0.0 - 1.0]")
    risk_tier: str = Field(description="CRITICAL, HIGH, MEDIUM, or LOW")
    archetype: str = Field(description="Identified behavioral protocol archetype")
    mechanistic_insight: str = Field(description="Forensic narrative explaining decision")
    fairness_metadata: FairnessMetadataResponse
    latent_manifolds: LatentManifoldsResponse
    shap_explanation: ShapExplanationResponse
    latency_ms: float


class BatchPredictionResponse(BaseModel):
    total_records: int
    fraud_count: int
    benign_count: int
    fraud_rate_pct: float
    predictions: List[SinglePredictionResponse]
    batch_latency_ms: float


class HealthCheckResponse(BaseModel):
    status: str
    project_id: str
    research_title: str
    publication_target: str
    pipeline_status: str
    champion_architecture: str
    features_active: int
    fairness_calibration: Dict[str, float]
    uptime_timestamp: float


# --------------------------------------------------------------------------------------
# FASTAPI LIFESPAN & INITIALIZATION
# --------------------------------------------------------------------------------------
pipeline: Optional[DeFiFraudInferencePipeline] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes the Champion Model A pipeline at startup."""
    global pipeline
    logger.info("Initializing Project DEFI-FRAUD-053 Inference Microservice...")
    try:
        pipeline = get_pipeline()
        logger.info("Champion Model A pipeline online and ready for incoming traffic.")
    except Exception as e:
        logger.error(f"Error during startup initialization: {e}", exc_info=True)
    yield
    logger.info("Shutting down DEFI-FRAUD-053 Inference Microservice.")


app = FastAPI(
    title="Project DEFI-FRAUD-053: Latent DeFi Fraud Detection Service",
    description=(
        "Production REST API for Phase 5 Application Deployment.\n\n"
        "**Research Artifact:** *Fairness-Constrained Ensemble Architectures for Latent Fraud Detection in DeFi Networks* (IEEE TIFS 2026).\n"
        "**Champion Architecture:** 4-Model Stacking Ensemble (XGBoost, LightGBM, Random Forest, Extra Trees) + "
        "Lagrangian Demographic Parity Fairness Calibration + Unsupervised Manifold Extractor (UMAP & Isolation Forest) + Tree-SHAP Explainability."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Web Dashboard & Microservice Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------------------------------------------
# ENDPOINTS
# --------------------------------------------------------------------------------------

@app.get("/", tags=["Root"])
async def root_index():
    """Service landing page and navigation catalog."""
    return {
        "service": "Project DEFI-FRAUD-053 Forensic Intelligence Microservice",
        "version": "1.0.0",
        "status": "ONLINE",
        "target_venue": "IEEE Transactions on Information Forensics and Security (IEEE TIFS, 2026)",
        "documentation": "/docs",
        "endpoints": {
            "healthcheck": "/healthcheck",
            "predict_json": "/predict",
            "predict_csv": "/predict/csv",
            "model_metadata": "/model/metadata",
            "presets": "/examples/{case_id}"
        }
    }


@app.get("/healthcheck", response_model=HealthCheckResponse, tags=["System Health"])
async def healthcheck():
    """
    Verifies service health, active ensemble components, fairness thresholds, and model readiness.
    """
    global pipeline
    if pipeline is None:
        pipeline = get_pipeline()

    return HealthCheckResponse(
        status="HEALTHY",
        project_id="DEFI-FRAUD-053",
        research_title="Fairness-Constrained Ensemble Architectures for Latent Fraud Detection in DeFi Networks",
        publication_target="IEEE Transactions on Information Forensics and Security (IEEE TIFS, 2026)",
        pipeline_status="ONLINE" if pipeline.is_ready else "INITIALIZING",
        champion_architecture="Stacking Ensemble (XGBoost + LightGBM + RF + ExtraTrees + Logistic Meta-Learner)",
        features_active=len(ALL_25_FEATURES),
        fairness_calibration=pipeline.fairness_thresholds,
        uptime_timestamp=time.time()
    )


@app.post("/predict", response_model=Union[SinglePredictionResponse, BatchPredictionResponse], tags=["Forensic Inference"])
async def predict_transaction(payload: Union[RawTransactionPayload, List[RawTransactionPayload], Dict[str, Any]]):
    """
    Primary inference endpoint: Ingests raw or unformatted on-chain ledger features,
    processes them through the Champion Model A pipeline, and returns predictions,
    calibrated probabilities, Lagrangian fairness tiers, and local Tree-SHAP attributions.
    """
    global pipeline
    if pipeline is None:
        pipeline = get_pipeline()

    try:
        # Handle single dictionary or Pydantic model
        if isinstance(payload, RawTransactionPayload):
            raw_dict = payload.model_dump(by_alias=True)
            result = pipeline.predict_single(raw_dict)
            return SinglePredictionResponse(**result)

        elif isinstance(payload, dict):
            # If payload is a dictionary wrapping a list or single record
            if "transactions" in payload and isinstance(payload["transactions"], list):
                t_start = time.perf_counter()
                results = [pipeline.predict_single(tx if isinstance(tx, dict) else tx.model_dump(by_alias=True)) for tx in payload["transactions"]]
                fraud_count = sum(1 for r in results if r["prediction"] == 1)
                batch_ms = (time.perf_counter() - t_start) * 1000.0
                return BatchPredictionResponse(
                    total_records=len(results),
                    fraud_count=fraud_count,
                    benign_count=len(results) - fraud_count,
                    fraud_rate_pct=round((fraud_count / len(results)) * 100.0, 2) if results else 0.0,
                    predictions=[SinglePredictionResponse(**r) for r in results],
                    batch_latency_ms=round(batch_ms, 2)
                )
            else:
                result = pipeline.predict_single(payload)
                return SinglePredictionResponse(**result)

        elif isinstance(payload, list):
            t_start = time.perf_counter()
            results = [pipeline.predict_single(tx.model_dump(by_alias=True) if isinstance(tx, RawTransactionPayload) else tx) for tx in payload]
            fraud_count = sum(1 for r in results if r["prediction"] == 1)
            batch_ms = (time.perf_counter() - t_start) * 1000.0
            return BatchPredictionResponse(
                total_records=len(results),
                fraud_count=fraud_count,
                benign_count=len(results) - fraud_count,
                fraud_rate_pct=round((fraud_count / len(results)) * 100.0, 2) if results else 0.0,
                predictions=[SinglePredictionResponse(**r) for r in results],
                batch_latency_ms=round(batch_ms, 2)
            )

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported payload structure. Provide a valid JSON transaction object or array."
            )

    except Exception as e:
        logger.error(f"Inference error during /predict execution: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference pipeline execution failure: {str(e)}"
        )


@app.post("/predict/csv", response_model=BatchPredictionResponse, tags=["Batch Auditing"])
async def predict_from_csv(file: UploadFile = File(...)):
    """
    Accepts an uploaded CSV file containing raw Ethereum ledger transaction rows,
    parses each record, runs batch inference, and returns complete forensic results.
    """
    global pipeline
    if pipeline is None:
        pipeline = get_pipeline()

    if not file.filename.endswith(('.csv', '.txt')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Upload a valid CSV document."
        )

    try:
        t_start = time.perf_counter()
        contents = await file.read()
        df_uploaded = pd.read_csv(io.BytesIO(contents))
        
        if df_uploaded.empty:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded CSV contains no rows.")

        results = []
        for _, row in df_uploaded.iterrows():
            res = pipeline.predict_single(row.to_dict())
            results.append(SinglePredictionResponse(**res))

        fraud_count = sum(1 for r in results if r.prediction == 1)
        batch_ms = (time.perf_counter() - t_start) * 1000.0

        return BatchPredictionResponse(
            total_records=len(results),
            fraud_count=fraud_count,
            benign_count=len(results) - fraud_count,
            fraud_rate_pct=round((fraud_count / len(results)) * 100.0, 2),
            predictions=results,
            batch_latency_ms=round(batch_ms, 2)
        )

    except Exception as e:
        logger.error(f"CSV ingestion error: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to process CSV: {str(e)}")


@app.get("/examples/{case_id}", tags=["Forensic Preset Edge Cases"])
async def get_preset_edge_case(case_id: int = Path(..., ge=1, le=3, description="Edge case index (1=Stealth Sybil, 2=DEX LP, 3=Flash Arbitrage)")):
    """
    Returns curated IEEE TIFS DeFi benchmark edge case transaction payloads.
    """
    presets = {
        1: {
            "title": "Case 1: Stealth Sybil / Rapid Token Draining Exploit",
            "archetype": "Stealth Sybil",
            "payload": {
                "Avg min between sent tnx": 12.4,
                "Avg min between received tnx": 5.8,
                "Time Diff between first and last (Mins)": 1420.0,  # ~1 day lifespan
                "Unique Received From Addresses": 3,
                "Unique Sent To Addresses": 18,
                "min value received": 0.05,
                "max value received": 2.5,
                "avg val received": 0.85,
                "min val sent": 0.02,
                "max val sent": 1.2,
                "avg val sent": 0.45,
                "Total ERC20 tnxs": 4.0,
                "ERC20 total Ether sent contract": 0.0,
                "ERC20 uniq sent addr": 2.0,
                "ERC20 uniq rec addr": 2.0,
                "ERC20 uniq sent addr.1": 0.0,
                "ERC20 min val rec": 0.0,
                "ERC20 avg val rec": 120.5,
                "ERC20 uniq sent token name": 1.0,
                "ERC20 most sent token type": "0",
                "ERC20_most_rec_token_type": "0",
                "anomaly_score": -0.2850,
                "UMAP_1": 3.12,
                "UMAP_2": 8.45,
                "UMAP_3": 14.10
            }
        },
        2: {
            "title": "Case 2: High-Frequency DEX Liquidity Provider",
            "archetype": "DEX Liquidity Provider",
            "payload": {
                "Avg min between sent tnx": 145.2,
                "Avg min between received tnx": 89.4,
                "Time Diff between first and last (Mins)": 485000.0,  # ~336 days lifespan
                "Unique Received From Addresses": 45,
                "Unique Sent To Addresses": 112,
                "min value received": 0.0,
                "max value received": 150.0,
                "avg val received": 12.5,
                "min val sent": 0.0,
                "max val sent": 120.0,
                "avg val sent": 8.9,
                "Total ERC20 tnxs": 185.0,
                "ERC20 total Ether sent contract": 0.0,
                "ERC20 uniq sent addr": 25.0,
                "ERC20 uniq rec addr": 40.0,
                "ERC20 uniq sent addr.1": 0.0,
                "ERC20 min val rec": 0.0,
                "ERC20 avg val rec": 45000.0,
                "ERC20 uniq sent token name": 18.0,
                "ERC20 most sent token type": "Livepeer Token",
                "ERC20_most_rec_token_type": "Numeraire",
                "anomaly_score": 0.0450,
                "UMAP_1": 7.85,
                "UMAP_2": 3.20,
                "UMAP_3": 11.40
            }
        },
        3: {
            "title": "Case 3: High-Velocity Flash Arbitrage / MEV Bot",
            "archetype": "Flash Arbitrage Bot",
            "payload": {
                "Avg min between sent tnx": 0.45,  # Sub-minute burst
                "Avg min between received tnx": 1.20,
                "Time Diff between first and last (Mins)": 38400.0,  # ~26 days lifespan
                "Unique Received From Addresses": 8,
                "Unique Sent To Addresses": 4,
                "min value received": 1.0,
                "max value received": 500.0,
                "avg val received": 85.0,
                "min val sent": 0.5,
                "max val sent": 490.0,
                "avg val sent": 82.0,
                "Total ERC20 tnxs": 65.0,
                "ERC20 total Ether sent contract": 0.0,
                "ERC20 uniq sent addr": 4.0,
                "ERC20 uniq rec addr": 6.0,
                "ERC20 uniq sent addr.1": 0.0,
                "ERC20 min val rec": 10.0,
                "ERC20 avg val rec": 12500.0,
                "ERC20 uniq sent token name": 6.0,
                "ERC20 most sent token type": "Raiden",
                "ERC20_most_rec_token_type": "XENON",
                "anomaly_score": -0.0820,
                "UMAP_1": 6.10,
                "UMAP_2": 9.80,
                "UMAP_3": 15.20
            }
        }
    }
    if case_id not in presets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Case ID {case_id} not found. Choose 1, 2, or 3.")
    return presets[case_id]


@app.get("/model/metadata", tags=["Model Governance & Ablation"])
async def get_model_metadata():
    """
    Returns IEEE TIFS publication metadata, 5-fold cross-validation performance,
    ablation study degradation deltas, and Lagrangian fairness guarantees.
    """
    return {
        "project": "DEFI-FRAUD-053",
        "title": "Fairness-Constrained Ensemble Architectures for Latent Fraud Detection in DeFi Networks",
        "champion_model": "Model A (Full Architecture)",
        "ablation_benchmarking": {
            "Model A (Full Q1 Architecture)": {"F1": 0.9974, "ROC_AUC": 0.9996, "Disparate_Impact": 0.9652, "Delta_F1": "0.00%"},
            "Model B (Minus Latent Manifolds)": {"F1": 0.9785, "ROC_AUC": 0.9912, "Disparate_Impact": 0.9410, "Delta_F1": "-1.89%"},
            "Model C (Single Baseline Unconstrained)": {"F1": 0.9492, "ROC_AUC": 0.9784, "Disparate_Impact": 0.7845, "Delta_F1": "-4.83%"},
            "Model D (Ensemble minus Fairness)": {"F1": 0.9961, "ROC_AUC": 0.9994, "Disparate_Impact": 0.8812, "Delta_F1": "-0.13%"},
            "Model E (Single Model with Latents)": {"F1": 0.9925, "ROC_AUC": 0.9982, "Disparate_Impact": 0.9120, "Delta_F1": "-0.49%"}
        },
        "fairness_guarantees": {
            "law_standard": "US EEOC 4/5ths Rule (Disparate Impact >= 0.80)",
            "demographic_parity_gap": 0.0148,
            "equalized_odds_gap": 0.0112,
            "status": "FULLY_CERTIFIED_COMPLIANT"
        }
    }


# --------------------------------------------------------------------------------------
# SERVERLESS ASGI HANDLER (VERCEL / AWS LAMBDA)
# --------------------------------------------------------------------------------------
try:
    from mangum import Mangum
    handler = Mangum(app)
except ImportError:
    handler = app


# --------------------------------------------------------------------------------------
# CLI ENTRY POINT
# --------------------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    logger.info("Launching FastAPI Backend on http://0.0.0.0:8000...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

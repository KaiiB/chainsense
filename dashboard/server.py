#!/usr/bin/env python3
"""
Chainsense Dashboard Backend API
Serves analysis data from the notebook output
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from pathlib import Path
import json
from typing import List, Dict, Any
import math

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = Path(__file__).parent.parent / "data" / "gold" / "wallet_features_with_clusters.parquet"

def sanitize_for_json(obj):
    """Recursively convert NaN/inf values into JSON-safe None."""
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(v) for v in obj]
    elif isinstance(obj, tuple):
        return [sanitize_for_json(v) for v in obj]
    elif isinstance(obj, (np.floating, float)):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return float(obj)
    elif isinstance(obj, (np.integer, int)):
        return int(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif pd.isna(obj):
        return None
    else:
        return obj
    

def load_analysis_data() -> Dict[str, Any]:
    """Load and prepare analysis data from parquet file."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Data file not found at {DATA_PATH}")
    
    df = pd.read_parquet(DATA_PATH)
    
    # Prepare wallet data
    wallets = df.to_dict('records')
    
    # Compute cluster statistics
    cluster_stats = []
    for cluster_id in sorted(df['cluster_id'].unique()):
        cluster_data = df[df['cluster_id'] == cluster_id]
        stats = {
            'cluster_id': int(cluster_id),
            'count': len(cluster_data),
            'mean_eth_sent': float(cluster_data['eth_sent'].mean()),
            'mean_eth_recv': float(cluster_data['eth_recv'].mean()),
            'mean_counterparties': float(cluster_data['unique_counterparties'].mean()),
            'mean_contracts': float(cluster_data['unique_contracts'].mean()),
        }
        cluster_stats.append(stats)
    
    # Compute correlation matrix
    feature_cols = [c for c in df.columns if c not in ['wallet', 'cluster_id', 'pc1', 'pc2', 'ld1', 'ld2']]
    correlation = df[feature_cols].corr().values.tolist()
    
    # Placeholder silhouette score (should be computed in notebook)
    silhouette_score = 0.5
    
    return sanitize_for_json({
        'wallets': wallets,
        'cluster_stats': cluster_stats,
        'silhouette_score': silhouette_score,
        'n_clusters': len(cluster_stats),
        'correlation_matrix': correlation,
        'feature_names': feature_cols,
    })

@app.get("/api/analysis")
async def get_analysis():
    """Endpoint to fetch analysis data."""
    try:
        data = load_analysis_data()
        return data
    except Exception as e:
        return {"error": str(e)}, 500

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

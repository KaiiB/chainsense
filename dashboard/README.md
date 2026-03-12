# Chainsense Dashboard

A clean, minimalistic frontend for exploring Ethereum wallet clustering analysis results.

## Features

- **PCA & LDA Projections**: Interactive scatter plots of dimensionality-reduced data
- **Cluster Visualization**: Color-coded wallet clusters with filtering
- **Feature Correlation**: Heatmap of feature correlations
- **Cluster Statistics**: Summary tables by cluster group
- **Silhouette Score**: Quality metric for clustering
- **Interpretation**: Detailed analysis and findings

## Tech Stack

- **Frontend**: React 18 + TypeScript
- **Visualization**: D3.js
- **Build**: Vite
- **Styling**: CSS with Times New Roman font
- **Backend**: FastAPI (Python)

## Getting Started

### Prerequisites

- Node.js 16+
- Python 3.8+

### Frontend Setup

```bash
cd dashboard
npm install
npm run dev
```

Runs on `http://localhost:5173`

### Backend Setup

```bash
pip install fastapi uvicorn pandas pyarrow numpy
python dashboard/server.py
```

Runs on `http://localhost:8000`

## Data Flow

1. Notebook generates `data/gold/wallet_features_with_clusters.parquet`
2. Backend API reads parquet file and serves JSON
3. Frontend fetches data and renders interactive visualizations

## UI Layout

- **Header**: Title and description
- **Stats Row**: Key metrics (total wallets, clusters, silhouette score)
- **Controls**: Cluster filter dropdown
- **Tabs**: 
  - Overview (cluster statistics table)
  - PCA Projection (3D scatter)
  - LDA Projection (2D scatter)
  - Feature Correlation (heatmap)
  - Interpretation (findings and analysis)

## Design Philosophy

- **Minimalist**: Clean, spacious layout with subtle shadows
- **Typography-focused**: Times New Roman serif font for academic feel
- **Data-first**: Visualizations are the focus, minimal chrome
- **Responsive**: Adapts to various screen sizes
- **Accessible**: High contrast, clear labels

## API Contract

### GET /api/analysis

Response:
```json
{
  "wallets": [
    {
      "wallet": "0x...",
      "tx_count": 123,
      "eth_sent": 45.67,
      "eth_recv": 89.01,
      "cluster_id": 0,
      "pc1": 12.34,
      "pc2": -5.67,
      "ld1": 1.23,
      "ld2": -4.56,
      ...
    }
  ],
  "cluster_stats": [
    {
      "cluster_id": 0,
      "count": 1000,
      "mean_tx_count": 123.45,
      ...
    }
  ],
  "silhouette_score": 0.534,
  "n_clusters": 2,
  "correlation_matrix": [...],
  "feature_names": ["tx_count", "eth_sent", ...]
}
```

## Building for Production

```bash
npm run build
```

Creates optimized bundle in `dist/`

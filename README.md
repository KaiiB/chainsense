# Chainsense

Official repo for TQT x DS3 Project Chainsense. 

This project attempts to explore the blockchain hidden world, uncovering secrets behind encrypted cryptocurrency transactions and attempting to decipher rows of hidden data.

## Pipeline Overview

The **Chainsense Feature Space** pipeline transforms raw Ethereum transaction data into interpretable wallet clusters, enabling analysis of behavioral patterns and wallet classification.

### Architecture

```
Raw Transactions (Parquet)
         ↓
    Feature Engineering (15 features)
         ↓
    Preprocessing (log1p + RobustScaler)
         ↓
    Dimensionality Reduction (PCA/LDA)
         ↓
    Clustering (HDBSCAN)
         ↓
    Statistical Analysis & Visualization
         ↓
    Dashboard-ready Artifacts
```

### 1) Data Ingestion
- **Source**: Local parquet file (`data/bronze/transactions.parquet`) or live Alchemy API
- **Required columns**: `block_number`, `from`, `to`, `value`, `gas`, `gas_price`
- **Top wallets**: Filtered to top 2,000 by total transaction participation

### 2) Feature Engineering (15-Feature Schema)

#### Activity Features
- `tx_count`: Total transactions (sent + received)
- `active_blocks`: Number of unique blocks wallet appears in
- `tx_per_block`: Average transactions per active block
- `burstiness`: Standard deviation of tx count per block (temporal clustering)

#### Value Flow Features
- `eth_sent`: Total ETH value sent
- `eth_recv`: Total ETH value received
- `eth_net_flow`: Net ETH flow (received - sent)
- `avg_tx_value`: Mean transaction value

#### Gas Behavior Features
- `avg_gas`: Average gas per transaction
- `total_gas_spent_eth`: Total ETH spent on gas

#### Interaction Features
- `unique_counterparties`: Distinct addresses interacted with
- `unique_contracts`: Distinct smart contracts interacted with
- `contract_interaction_rate`: Fraction of transactions to contracts
- `counterparty_concentration`: Herfindahl index of counterparty interactions

### 3) Preprocessing
- **Log transformation**: Heavy-tailed features (activity, value, gas) normalized via `log1p()`
- **Robust scaling**: RobustScaler applied to handle outliers
- **Result**: Scaled feature matrix `Xs` ready for clustering

### 4) Dimensionality Reduction
- **PCA**: 3-component projection for visualization and analysis
- **LDA**: 2-component discriminant analysis for cluster separation
- **Interactive 3D plot**: Plotly-based exploration of wallet distribution

### 5) Clustering
- **Algorithm**: HDBSCAN (density-based hierarchical clustering)
- **Advantages**: Automatically discovers optimal number of clusters, identifies noise points
- **Output**: Cluster labels + noise point detection

### 6) Analysis & Interpretation
- **Edge vs. Center Analysis**: Identifies peripheral vs. core wallets in PCA space
- **Feature Distributions**: Visualizes marginal distributions by cluster
- **Statistical Summaries**: Cluster-wise medians, means, and quartiles
- **Profile Labels**: Interpretable categories (e.g., whale-like, bot-like, router)

### 7) Artifacts
- **Gold layer output**: `data/gold/wallet_features_with_clusters.parquet`
  - Includes: Original features + cluster assignments + PCA/LDA projections
  - Ready for downstream dashboard and analysis

## Key Insights

### Cluster Profiles
- **Cluster 0 (Regular Traders)**: Concentrated center, uniform patterns, predictable behavior
- **Cluster 1 (Diverse Actors)**: Peripheral edges, high variance, includes whales & bots
- **Noise Points**: Edge cases and extreme outliers

### Edge vs. Center
- **75th percentile distance**: Separates core from periphery
- **Edge wallets**: 2-3x higher variance in most features
- **Center wallets**: More homogeneous, likely institutional or steady-state participants

## Usage

### Running the Pipeline
```bash
jupyter notebook chainsense_feature_space.ipynb
```

1. Ensure `data/bronze/transactions.parquet` exists or configure Alchemy API
2. Run cells sequentially (1-10)
3. Review cluster visualizations and statistics
4. Output automatically saved to `data/gold/`

### Key Parameters
- `TOP_K_WALLETS`: Number of wallets to analyze (default: 2,000)
- `K_RANGE`: KMeans k values for silhouette analysis (unused with HDBSCAN)
- `RANDOM_STATE`: Reproducibility seed (default: 42)

## Dependencies
- pandas, numpy, scikit-learn
- hdbscan (density-based clustering)
- matplotlib, plotly (visualization)

## Future Work
- Integration with blockchain RPC for real-time data
- Behavioral classification (MEV extractors, arbitrageurs, etc.)
- Temporal clustering (wallet evolution over time)
- Network analysis (transaction graph properties) 

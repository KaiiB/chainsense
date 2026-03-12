export interface Wallet {
  wallet: string;
  tx_count: number;
  tx_per_block: number;
  burstiness: number;
  eth_sent: number;
  eth_recv: number;
  avg_tx_value: number;
  avg_gas: number;
  total_gas_spent_eth: number;
  unique_counterparties: number;
  unique_contracts: number;
  pc1: number;
  pc2: number;
  ld1: number;
  ld2: number;
  cluster_id: number;
}

export interface ClusterStats {
  cluster_id: number;
  count: number;
  mean_tx_count: number;
  mean_eth_sent: number;
  mean_eth_recv: number;
  mean_burstiness: number;
  mean_counterparties: number;
  mean_contracts: number;
}

export interface AnalysisData {
  wallets: Wallet[];
  cluster_stats: ClusterStats[];
  silhouette_score: number;
  n_clusters: number;
  correlation_matrix: number[][];
  feature_names: string[];
}

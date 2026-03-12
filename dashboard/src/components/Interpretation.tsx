import React from 'react';

interface InterpretationProps {
  clusterCount: number;
  silhouetteScore: number;
  noiseCount: number;
}

export const Interpretation: React.FC<InterpretationProps> = ({
  clusterCount,
  silhouetteScore,
  noiseCount
}) => {
  return (
    <div className="card interpretation">
      <h2>Project Interpretation & Findings</h2>
      
      <h4>Clustering Results</h4>
      <p>
        HDBSCAN identified <strong>{clusterCount} natural clusters</strong> in the Ethereum wallet feature space.
        The silhouette score of <strong>{silhouetteScore.toFixed(3)}</strong> indicates the quality of cluster separation
        (ranges from -1 to 1, higher is better).
      </p>

      <h4>Cluster Profiles</h4>
      <ul>
        <li>
          <strong>Cluster 0 (Center, Purple):</strong> Wallets with consistent, predictable behavior.
          Characterized by lower variance in transaction counts, eth flows, and burstiness.
          Likely represents regular traders, staking pools, or institutional accounts.
        </li>
        <li>
          <strong>Cluster 1 (Periphery, Yellow):</strong> Diverse wallet archetypes with high behavioral variance.
          Includes whale wallets, arbitrage bots, MEV extractors, and exchange addresses.
          Shows bimodal or extreme distributions in most features.
        </li>
        {noiseCount > 0 && (
          <li>
            <strong>Noise Points ({noiseCount} wallets):</strong> Edge-case wallets that don't conform to either cluster's
            density structure. Often extreme outliers in feature space combinations.
          </li>
        )}
      </ul>

      <h4>Feature Differentiation</h4>
      <ul>
        <li><strong>Transaction Activity:</strong> Cluster 1 shows heavier right tail—more high-volume wallets</li>
        <li><strong>ETH Flow:</strong> Cluster 1 exhibits bimodal distributions (senders vs. receivers)</li>
        <li><strong>Burstiness:</strong> Cluster 1 wallets are more temporally clustered (bursty behavior)</li>
        <li><strong>Gas Spending:</strong> Cluster 1 shows higher variance and absolute gas costs</li>
        <li><strong>Interaction Diversity:</strong> Cluster 1 interacts with more counterparties and contracts</li>
      </ul>

      <h4>Edge vs. Center Analysis</h4>
      <ul>
        <li>Points on the <strong>periphery of PCA space</strong> (75th+ percentile distance) are predominantly Cluster 1</li>
        <li><strong>Center wallets</strong> form a tight, homogeneous group in feature space</li>
        <li><strong>Periphery wallets</strong> are dispersed, indicating diverse behavioral profiles</li>
      </ul>

      <h4>Project Conclusions</h4>
      <ul>
        <li>
          Ethereum wallets naturally segregate into two primary behavioral archetypes: 
          <strong>steady-state actors</strong> vs. <strong>diverse/volatile participants</strong>
        </li>
        <li>
          Whale wallets, bot networks, and high-variance actors cluster together in periphery, 
          suggesting shared behavioral complexity
        </li>
        <li>
          Feature space visualization enables rapid wallet classification and anomaly detection 
          for on-chain forensics and risk assessment
        </li>
        <li>
          The density-based clustering approach (HDBSCAN) effectively captures natural structure 
          without requiring pre-specified cluster counts
        </li>
      </ul>
    </div>
  );
};

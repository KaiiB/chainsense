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
        HDBSCAN identified <strong>{clusterCount} natural clusters</strong> in
        the Ethereum wallet feature space. The silhouette score of{' '}
        <strong>{silhouetteScore.toFixed(3)}</strong> indicates cluster quality
        (ranges from -1 to 1, higher is better).
        {noiseCount > 0 && ` ${noiseCount} wallets were labeled as noise —
        too behaviorally unique to fit any cluster.`}
      </p>

      <h4>Cluster Profiles</h4>
      <p>
        Wallets were grouped into <strong>{clusterCount} behavioral 
        archetypes</strong> based on transaction activity, ETH flow, gas 
        usage, and interaction patterns. Each cluster represents a distinct 
        type of Ethereum user behavior.
      </p>

      <h4>Feature Differentiation</h4>
      <ul>
        <li><strong>Transaction Activity:</strong> High volume wallets separate clearly from typical users</li>
        <li><strong>ETH Flow:</strong> Whales and protocols show extreme sent/received values</li>
        <li><strong>Gas Spending:</strong> Bots and automated wallets show distinct gas patterns</li>
        <li><strong>Interaction Diversity:</strong> Contract interaction rate separates automated from human wallets</li>
        <li><strong>Counterparties:</strong> Bots tend to interact with very few addresses repeatedly</li>
      </ul>

      <h4>Edge vs. Center Analysis</h4>
      <ul>
        <li>Wallets on the <strong>periphery of PCA space</strong> show high variance across most features</li>
        <li><strong>Center wallets</strong> form a tight homogeneous group — likely regular retail users</li>
        <li><strong>Edge wallets</strong> include whales, bots, and major protocol contracts</li>
      </ul>

      <h4>Project Conclusions</h4>
      <ul>
        <li>Ethereum wallets naturally segregate into behavioral archetypes detectable through unsupervised ML</li>
        <li>HDBSCAN effectively captures natural structure without pre-specified cluster counts</li>
        <li>High noise rate (~54%) suggests significant behavioral diversity in the top 1,000 wallets</li>
        <li>Feature space visualization enables rapid wallet classification and anomaly detection</li>
        <li>Giant protocol contracts (e.g. USDT, Uniswap) dominate PC1 — filtering them could improve cluster quality</li>
      </ul>
    </div>
  );
};
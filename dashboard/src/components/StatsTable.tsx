import React from 'react';
import { Wallet, ClusterStats } from '../types';

interface StatsTableProps {
  stats: ClusterStats[];
  wallets: Wallet[];
}

export const StatsTable: React.FC<StatsTableProps> = ({ stats, wallets }) => {
  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Cluster</th>
            <th>Wallets</th>
            <th>Avg ETH Sent</th>
            <th>Avg ETH Recv</th>
            <th>Avg Counterparties</th>
            <th>Avg Contracts</th>
          </tr>
        </thead>
        <tbody>
          {stats.map(s => (
            <tr key={s.cluster_id}>
              <td><strong>{s.cluster_id}</strong></td>
              <td>{s.count}</td>
              <td>{s.mean_eth_sent.toFixed(4)}</td>
              <td>{s.mean_eth_recv.toFixed(4)}</td>
              <td>{s.mean_counterparties.toFixed(2)}</td>
              <td>{s.mean_contracts.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

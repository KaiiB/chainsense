import React, { useState, useEffect } from 'react';
import { AnalysisData } from '../types';
import { ScatterChart } from './ScatterChart';
import { Heatmap } from './Heatmap';
import { StatsTable } from './StatsTable';
import { Interpretation } from './Interpretation';

interface AppProps {
  data: AnalysisData;
}

type ViewType = 'overview' | 'pca' | 'lda' | 'correlation' | 'interpretation';

export const Dashboard: React.FC<AppProps> = ({ data }) => {
  const [activeView, setActiveView] = useState<ViewType>('overview');
  const [selectedCluster, setSelectedCluster] = useState<number | null>(null);

  const noiseCount = data.wallets.filter(w => w.cluster_id === -1).length;
  const filteredWallets = selectedCluster !== null 
    ? data.wallets.filter(w => w.cluster_id === selectedCluster)
    : data.wallets;

  return (
    <div>
      <header>
        <h1>Chainsense Dashboard</h1>
        <p>Ethereum wallet behavioral clustering and analysis</p>
      </header>

      <div className="container">
        {/* Stats Row */}
        <div className="stats-grid">
          <div className="stat-box">
            <div className="stat-value">{data.wallets.length}</div>
            <div className="stat-label">Total Wallets</div>
          </div>
          <div className="stat-box">
            <div className="stat-value">{data.n_clusters}</div>
            <div className="stat-label">Clusters Found</div>
          </div>
          <div className="stat-box">
            <div className="stat-value">{data.silhouette_score.toFixed(3)}</div>
            <div className="stat-label">Silhouette Score</div>
          </div>
          <div className="stat-box">
            <div className="stat-value">{noiseCount}</div>
            <div className="stat-label">Noise Points</div>
          </div>
        </div>

        {/* Cluster Filter */}
        <div className="controls">
          <label>Filter by Cluster:</label>
          <select value={selectedCluster === null ? '' : selectedCluster} onChange={e => setSelectedCluster(e.target.value === '' ? null : parseInt(e.target.value))}>
            <option value="">All Wallets</option>
            {data.cluster_stats.map(s => (
              <option key={s.cluster_id} value={s.cluster_id}>
                Cluster {s.cluster_id} ({s.count} wallets)
              </option>
            ))}
            {noiseCount > 0 && <option value={-1}>Noise Points ({noiseCount})</option>}
          </select>
        </div>

        {/* Navigation Tabs */}
        <div className="tabs">
          <button 
            className={`tab ${activeView === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveView('overview')}
          >
            Overview
          </button>
          <button 
            className={`tab ${activeView === 'pca' ? 'active' : ''}`}
            onClick={() => setActiveView('pca')}
          >
            PCA Projection
          </button>
          <button 
            className={`tab ${activeView === 'lda' ? 'active' : ''}`}
            onClick={() => setActiveView('lda')}
          >
            LDA Projection
          </button>
          <button 
            className={`tab ${activeView === 'correlation' ? 'active' : ''}`}
            onClick={() => setActiveView('correlation')}
          >
            Feature Correlation
          </button>
          <button 
            className={`tab ${activeView === 'interpretation' ? 'active' : ''}`}
            onClick={() => setActiveView('interpretation')}
          >
            Interpretation
          </button>
        </div>

        {/* Content */}
        {activeView === 'overview' && (
          <div className="grid grid-1">
            <div className="card">
              <h2>Cluster Statistics</h2>
              <StatsTable stats={data.cluster_stats} wallets={data.wallets} />
            </div>
          </div>
        )}

        {activeView === 'pca' && (
          <div className="grid grid-1">
            <div className="card">
              <h2>PCA Projection (PC1 vs PC2)</h2>
              <div className="chart-container">
                <ScatterChart 
                  data={filteredWallets}
                  xField="pc1"
                  yField="pc2"
                  title="Principal Component Analysis"
                  colorField="cluster_id"
                />
              </div>
            </div>
          </div>
        )}

        {activeView === 'lda' && (
          <div className="grid grid-1">
            <div className="card">
              <h2>LDA Projection (LD1 vs LD2)</h2>
              <div className="chart-container">
                <ScatterChart 
                  data={filteredWallets}
                  xField="ld1"
                  yField="ld2"
                  title="Linear Discriminant Analysis"
                  colorField="cluster_id"
                />
              </div>
            </div>
          </div>
        )}

        {activeView === 'correlation' && (
          <div className="grid grid-1">
            <div className="card">
              <h2>Feature Correlation Matrix</h2>
              <div className="chart-container small">
                <Heatmap 
                  data={data.correlation_matrix}
                  labels={data.feature_names}
                  title="Pearson Correlation"
                />
              </div>
            </div>
          </div>
        )}

        {activeView === 'interpretation' && (
          <Interpretation 
            clusterCount={data.n_clusters}
            silhouetteScore={data.silhouette_score}
            noiseCount={noiseCount}
          />
        )}
      </div>
    </div>
  );
};

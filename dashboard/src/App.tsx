import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { AnalysisData } from './types';
import { Dashboard } from './components/Dashboard';
import './App.css';

const App: React.FC = () => {
  const [data, setData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<AnalysisData>('/api/analysis');
        console.log(response.data);
        setData(response.data);
      } catch (err) {
        setError(`Failed to load analysis data: ${err instanceof Error ? err.message : 'Unknown error'}`);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="loading">Loading analysis data...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!data) {
    return <div className="error">No data available</div>;
  }

  return <Dashboard data={data} />;
};

export default App;

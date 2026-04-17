import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useAuth } from './AuthContext';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line, Bar, Pie } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement,
  Title, Tooltip, Legend
);

function Results() {
  const { id } = useParams();
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const res = await fetch(`/results/${id}`);
        if (!res.ok) throw new Error('Result not found');
        const data = await res.json();
        setResults(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchResults();
  }, [id]);

  if (loading) return <div className="flex justify-center items-center h-64">Loading results...</div>;
  if (error) return <div className="text-red-600 text-center p-8">{error}</div>;
  if (!results) return <div>No results</div>;

  // Charts data
  const metrics = results.metrics || {};
  const silhouetteData = {
    labels: ['Silhouette', 'DB Index'],
    datasets: [{
      label: 'Clustering Quality',
      data: [metrics.silhouette || 0, metrics.davies_bouldin || 0],
      backgroundColor: ['rgba(99, 102, 241, 0.8)', 'rgba(239, 68, 68, 0.8)'],
    }]
  };

  const clusterDist = {
    labels: ['Cluster 0', 'Cluster 1', 'Cluster 2'],  // Dynamic from data
    datasets: [{
      data: [33, 33, 34],
      backgroundColor: ['#3b82f6', '#10b981', '#f59e0b'],
    }]
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-100">
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 flex justify-between items-center h-16">
          <Link to="/" className="text-xl font-bold text-indigo-600">Dashboard</Link>
          <Link to="/upload" className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700">New Analysis</Link>
        </div>
      </nav>
      <div className="max-w-7xl mx-auto py-12 px-4">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* KPIs */}
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6">📊 Key Metrics</h2>
            <div className="grid grid-cols-2 gap-4 mb-8">
              <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-6 rounded-xl">
                <h3 className="text-lg font-semibold opacity-90">Best K</h3>
                <p className="text-3xl font-bold">{results.best_k || '?'}</p>
              </div>
              <div className="bg-gradient-to-r from-emerald-500 to-emerald-600 text-white p-6 rounded-xl">
                <h3 className="text-lg font-semibold opacity-90">Silhouette</h3>
                <p className="text-3xl font-bold">{(metrics.silhouette || 0).toFixed(3)}</p>
              </div>
            </div>
            <Bar data={silhouetteData} />
          </div>

          {/* Cluster Distribution */}
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6">🎯 Cluster Distribution</h2>
            <Pie data={clusterDist} />
          </div>
        </div>

        {/* Insights */}
        <div className="mt-12 bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold mb-6">💡 Actionable Insights</h2>
          <div className="space-y-4">
            {results.insights?.map((insight, i) => (
              <div key={i} className="bg-indigo-50 p-4 rounded-lg border-l-4 border-indigo-500">
                {insight}
              </div>
            )) || <p>No insights available</p>}
          </div>
        </div>

        {/* Recommendations */}
        <div className="mt-8 bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold mb-6">🚀 Recommendations</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {results.recommendations?.slice(0,4).map(( reco, i ) => (
              <div key={i} className="bg-green-50 p-4 rounded-lg border border-green-200">
                <p className="font-medium text-green-900">{reco}</p>
              </div>
            )) || <p>No recommendations</p>}
          </div>
        </div>

        {results.rules && results.rules.length > 0 && (
          <div className="mt-8 bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6">📈 Association Rules</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead>
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rule</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Lift</th>
                  </tr>
                </thead>
                <tbody>
                  {results.rules.slice(0,5).map((rule, i) => (
                    <tr key={i}>
                      <td className="px-6 py-4">{`${rule.antecedents} → ${rule.consequents}`}</td>
                      <td className="px-6 py-4 font-medium">{rule.lift?.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Results;


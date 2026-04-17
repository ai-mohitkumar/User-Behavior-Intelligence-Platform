import React, { useState, useEffect } from 'react';
import {
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, LineChart, Line, Cell
} from 'recharts';
import { Upload, Zap, Users, DollarSign, ShoppingCart, TrendingUp } from 'lucide-react';

interface AnalysisResults {
  status: string;
  algorithm: {
    selected: string;
    scores: {
      kmeans: number;
      dbscan: number;
      hierarchical: number;
    };
  };
  metrics: {
    silhouette: number;
    davies_bouldin: number;
    calinski_harabasz: number;
    icso_score: number;
  };
  clusters: Array<{
    id: number;
    label: string;
    size: number;
    percentage: number;
    avg_spending: number;
    avg_purchases: number;
    avg_engagement: number;
  }>;
  anomalies: {
    count: number;
    percentage: number;
  };
  recommendations: Array<{
    cluster_id: number;
    cluster_label: string;
    recommendations: string[];
  }>;
}

export const Dashboard: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<AnalysisResults | null>(null);
  const [selectedCluster, setSelectedCluster] = useState<number>(0);
  const [clusterData, setClusterData] = useState<any[]>([]);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://127.0.0.1:8003/analyze-intelligent', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setResults(data);
      generateClusterData(data);
    } catch (error) {
      console.error('Analysis failed:', error);
      alert('Analysis failed. Please check the file format.');
    } finally {
      setLoading(false);
    }
  };

  const generateClusterData = (data: AnalysisResults) => {
    // Generate scatter plot data from clusters
    const scatterData = data.clusters.flatMap((cluster, idx) => {
      return Array(Math.round(cluster.size / 10))
        .fill(null)
        .map(() => ({
          x: cluster.avg_spending + (Math.random() - 0.5) * 50,
          y: cluster.avg_purchases + (Math.random() - 0.5) * 5,
          cluster: cluster.id,
          label: cluster.label,
        }));
    });
    setClusterData(scatterData);
  };

  const colors = ['#FFD700', '#00CED1', '#9370DB', '#FF6B6B', '#4ECDC4'];

  if (!results) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-8">
        {/* Background decoration */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-0 right-0 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-10"></div>
          <div className="absolute bottom-0 left-0 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-10"></div>
        </div>

        <div className="relative z-10 max-w-2xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="flex items-center justify-center gap-3 mb-4">
              <Zap className="w-10 h-10 text-yellow-400" />
              <h1 className="text-4xl font-bold text-white">
                User Behavior Analytics
              </h1>
            </div>
            <p className="text-gray-400 text-lg">
              Upload your data to discover intelligent clustering insights
            </p>
          </div>

          {/* Upload Card */}
          <div className="bg-gradient-to-br from-blue-900/50 to-purple-900/50 backdrop-blur-xl border border-blue-500/30 rounded-2xl p-8 shadow-2xl">
            <div className="space-y-6">
              {/* File Input */}
              <div className="relative">
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleFileSelect}
                  className="hidden"
                  id="file-input"
                />
                <label
                  htmlFor="file-input"
                  className="flex items-center justify-center gap-3 p-8 border-2 border-dashed border-blue-400/50 rounded-xl cursor-pointer hover:border-blue-300 transition bg-blue-900/20 hover:bg-blue-900/40"
                >
                  <Upload className="w-6 h-6 text-blue-400" />
                  <span className="text-gray-300">
                    {file ? file.name : 'Click to upload CSV file'}
                  </span>
                </label>
              </div>

              {/* File Info */}
              {file && (
                <div className="flex items-center gap-2 p-4 bg-green-900/30 border border-green-500/30 rounded-lg">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-green-300">{file.name} selected</span>
                </div>
              )}

              {/* Analyze Button */}
              <button
                onClick={handleAnalyze}
                disabled={!file || loading}
                className={`w-full py-3 px-6 rounded-xl font-semibold flex items-center justify-center gap-2 transition ${
                  file && !loading
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white cursor-pointer'
                    : 'bg-gray-700 text-gray-400 cursor-not-allowed'
                }`}
              >
                <Zap className="w-5 h-5" />
                {loading ? 'Analyzing...' : 'Run Intelligent Analysis'}
              </button>

              {/* Info */}
              <p className="text-sm text-gray-400 text-center">
                Required columns: InvoiceNo, user_id, quantity, price
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-8">
      {/* Background decoration */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 right-0 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-10"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-10"></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Zap className="w-8 h-8 text-yellow-400" />
            <h1 className="text-3xl font-bold text-white">
              User Behavior Analytics Dashboard
            </h1>
          </div>
          <button
            onClick={() => {
              setResults(null);
              setFile(null);
            }}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
          >
            New Analysis
          </button>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[
            {
              label: 'Total Users',
              value: results.clusters.reduce((sum, c) => sum + c.size, 0),
              icon: Users,
              color: 'from-blue-600 to-blue-400',
            },
            {
              label: 'Avg Spending',
              value: '$' + (results.clusters.reduce((sum, c) => sum + c.avg_spending, 0) / results.clusters.length).toFixed(2),
              icon: DollarSign,
              color: 'from-green-600 to-green-400',
            },
            {
              label: 'Avg Orders',
              value: (results.clusters.reduce((sum, c) => sum + c.avg_purchases, 0) / results.clusters.length).toFixed(1),
              icon: ShoppingCart,
              color: 'from-orange-600 to-orange-400',
            },
            {
              label: 'ICSO Score',
              value: results.metrics.icso_score.toFixed(2),
              icon: TrendingUp,
              color: 'from-purple-600 to-purple-400',
            },
          ].map((metric, idx) => {
            const Icon = metric.icon;
            return (
              <div
                key={idx}
                className={`bg-gradient-to-br ${metric.color} bg-opacity-10 backdrop-blur-xl border border-white/10 rounded-xl p-6 hover:border-white/20 transition`}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-gray-400 text-sm">{metric.label}</p>
                    <p className="text-2xl font-bold text-white mt-2">{metric.value}</p>
                  </div>
                  <Icon className="w-8 h-8 text-yellow-400 opacity-50" />
                </div>
              </div>
            );
          })}
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Cluster Visualization */}
          <div className="lg:col-span-2 bg-gradient-to-br from-blue-900/50 to-purple-900/50 backdrop-blur-xl border border-blue-500/30 rounded-xl p-6">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <Zap className="w-5 h-5 text-yellow-400" />
              User Clusters
            </h2>

            <ResponsiveContainer width="100%" height={350}>
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis
                  dataKey="x"
                  type="number"
                  name="Total Spending ($)"
                  stroke="rgba(255,255,255,0.5)"
                />
                <YAxis
                  dataKey="y"
                  type="number"
                  name="Avg Orders"
                  stroke="rgba(255,255,255,0.5)"
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    border: '1px solid rgba(59, 130, 246, 0.5)',
                    borderRadius: '8px',
                    color: '#fff',
                  }}
                />
                <Legend />
                {results.clusters.map((cluster, idx) => (
                  <Scatter
                    key={idx}
                    name={`${cluster.label} (${cluster.size} users)`}
                    data={clusterData.filter((d) => d.cluster === cluster.id)}
                    fill={colors[idx % colors.length]}
                    fillOpacity={0.7}
                  />
                ))}
              </ScatterChart>
            </ResponsiveContainer>
          </div>

          {/* Controls & Recommendations */}
          <div className="space-y-6">
            {/* Controls */}
            <div className="bg-gradient-to-br from-blue-900/50 to-purple-900/50 backdrop-blur-xl border border-blue-500/30 rounded-xl p-6">
              <h3 className="text-lg font-bold text-white mb-4">⚙️ Controls</h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Select Cluster
                  </label>
                  <select
                    value={selectedCluster}
                    onChange={(e) => setSelectedCluster(Number(e.target.value))}
                    className="w-full bg-blue-900/50 border border-blue-400/30 rounded-lg px-4 py-2 text-white hover:border-blue-400 transition"
                  >
                    {results.clusters.map((cluster) => (
                      <option key={cluster.id} value={cluster.id}>
                        Cluster {cluster.id} - {cluster.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="p-4 bg-blue-900/30 rounded-lg border border-blue-400/30">
                  <p className="text-sm text-gray-400">Cluster Info</p>
                  <div className="mt-3 space-y-2">
                    <div className="flex justify-between text-white">
                      <span>Size:</span>
                      <span className="font-bold">
                        {results.clusters[selectedCluster]?.size} users
                      </span>
                    </div>
                    <div className="flex justify-between text-white">
                      <span>% of Total:</span>
                      <span className="font-bold">
                        {results.clusters[selectedCluster]?.percentage.toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Top Recommendations */}
            <div className="bg-gradient-to-br from-blue-900/50 to-purple-900/50 backdrop-blur-xl border border-blue-500/30 rounded-xl p-6">
              <h3 className="text-lg font-bold text-white mb-4">🎯 Recommendations</h3>

              <div className="space-y-3">
                {results.recommendations[selectedCluster]?.recommendations.slice(0, 5).map((rec, idx) => (
                  <div
                    key={idx}
                    className="p-3 bg-gradient-to-r from-blue-900/50 to-purple-900/50 border border-blue-400/20 rounded-lg hover:border-blue-400/50 transition cursor-pointer group"
                  >
                    <p className="text-sm text-gray-300 group-hover:text-white transition">
                      {idx + 1}. {rec}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Analysis Details */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Algorithm Selection */}
          <div className="bg-gradient-to-br from-blue-900/50 to-purple-900/50 backdrop-blur-xl border border-blue-500/30 rounded-xl p-6">
            <h3 className="text-lg font-bold text-white mb-4">🤖 Algorithm Selection</h3>

            <div className="space-y-3">
              {Object.entries(results.algorithm.scores).map(([algo, score]) => (
                <div key={algo} className="flex items-center justify-between">
                  <span className="text-gray-300 capitalize">{algo}</span>
                  <div className="flex items-center gap-3">
                    <div className="w-32 h-2 bg-gray-700 rounded-full overflow-hidden">
                      <div
                        className={`h-full ${
                          algo === results.algorithm.selected
                            ? 'bg-gradient-to-r from-blue-500 to-purple-500'
                            : 'bg-gray-500'
                        }`}
                        style={{ width: `${score * 100}%` }}
                      ></div>
                    </div>
                    <span className="text-white font-bold w-12 text-right">
                      {(score * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-4 p-3 bg-green-900/30 border border-green-500/30 rounded-lg">
              <p className="text-sm text-green-300">
                ✅ Selected: <span className="font-bold">{results.algorithm.selected.toUpperCase()}</span>
              </p>
            </div>
          </div>

          {/* Quality Metrics */}
          <div className="bg-gradient-to-br from-blue-900/50 to-purple-900/50 backdrop-blur-xl border border-blue-500/30 rounded-xl p-6">
            <h3 className="text-lg font-bold text-white mb-4">📊 Quality Metrics</h3>

            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-blue-900/30 rounded-lg">
                <span className="text-gray-300">Silhouette Score</span>
                <span className="font-bold text-white">{results.metrics.silhouette.toFixed(4)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-purple-900/30 rounded-lg">
                <span className="text-gray-300">Davies-Bouldin Index</span>
                <span className="font-bold text-white">{results.metrics.davies_bouldin.toFixed(4)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-indigo-900/30 rounded-lg">
                <span className="text-gray-300">Calinski-Harabasz Index</span>
                <span className="font-bold text-white">{results.metrics.calinski_harabasz.toFixed(2)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-orange-900/30 border border-orange-500/30 rounded-lg">
                <span className="text-gray-300">🔬 ICSO Score</span>
                <span className="font-bold text-orange-300">{results.metrics.icso_score.toFixed(4)}</span>
              </div>
            </div>
          </div>

          {/* Anomaly Detection */}
          <div className="bg-gradient-to-br from-blue-900/50 to-purple-900/50 backdrop-blur-xl border border-blue-500/30 rounded-xl p-6">
            <h3 className="text-lg font-bold text-white mb-4">⚠️ Anomaly Detection</h3>

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Anomalies Found</span>
                <span className="text-2xl font-bold text-red-400">
                  {results.anomalies.count}
                </span>
              </div>

              <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-red-500 to-orange-500"
                  style={{ width: `${results.anomalies.percentage}%` }}
                ></div>
              </div>

              <p className="text-sm text-gray-300">
                {results.anomalies.percentage.toFixed(2)}% of users show unusual behavior
              </p>
            </div>
          </div>

          {/* Cluster Distribution */}
          <div className="bg-gradient-to-br from-blue-900/50 to-purple-900/50 backdrop-blur-xl border border-blue-500/30 rounded-xl p-6">
            <h3 className="text-lg font-bold text-white mb-4">📊 Cluster Distribution</h3>

            <div className="space-y-3">
              {results.clusters.map((cluster, idx) => (
                <div
                  key={idx}
                  onClick={() => setSelectedCluster(cluster.id)}
                  className="p-3 bg-blue-900/30 rounded-lg border border-blue-400/20 hover:border-blue-400/50 cursor-pointer transition"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-semibold text-white">
                      Cluster {cluster.id}
                    </span>
                    <span className="text-sm text-gray-400">
                      {cluster.percentage.toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className={`h-full`}
                      style={{
                        background: `linear-gradient(to right, ${colors[idx % colors.length]}, ${colors[(idx + 1) % colors.length]})`,
                        width: `${cluster.percentage}%`,
                      }}
                    ></div>
                  </div>
                  <p className="text-xs text-gray-400 mt-2">{cluster.size} users</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from './AuthContext';

function Upload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [resultId, setResultId] = useState(null);
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError('');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResultId(res.data.result_id);
      navigate(`/results/${res.data.result_id}`);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 flex justify-between items-center h-16">
          <h1 className="text-xl font-bold">Analyze Dataset</h1>
          <div>
            <button onClick={() => navigate('/')} className="mr-4 text-indigo-600 hover:underline">Dashboard</button>
            <button onClick={logout} className="text-gray-500 hover:text-gray-700">Logout</button>
          </div>
        </div>
      </nav>
      <div className="max-w-2xl mx-auto py-12 px-4">
        <div className="bg-white shadow-xl rounded-lg p-8">
          <h2 className="text-3xl font-bold mb-6">Upload CSV Dataset</h2>
          {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">{error}</div>}
          <form onSubmit={handleUpload} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                CSV File (user behavior data)
              </label>
              <input
                type="file"
                accept=".csv"
                onChange={(e) => setFile(e.target.files[0])}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
                required
              />
              <p className="mt-2 text-sm text-gray-500">
                Expected columns: quantity, price, InvoiceNo, Description (for patterns)
              </p>
            </div>
            <button
              type="submit"
              disabled={!file || loading}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Analyzing...' : 'Run Intelligence Analysis'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Upload;


import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from './AuthContext';

function Dashboard() {
  const { logout, user } = useAuth();

  return (
    <div className="min-h-screen">
      <nav className="bg-white shadow-lg dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">🧠 User Behavior Intelligence</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link to="/upload" className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700">
                📊 Upload & Analyze
              </Link>
              <button onClick={logout} className="text-gray-500 hover:text-gray-700 dark:text-gray-400">
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-4xl font-extrabold text-gray-900 dark:text-white sm:text-5xl">
            Welcome to your Dashboard
          </h2>
          <p className="mt-4 text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Upload user behavior datasets to get intelligent clustering, pattern mining, and personalized recommendations.
          </p>
          <div className="mt-10">
            <Link
              to="/upload"
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Get Started with Analysis
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;


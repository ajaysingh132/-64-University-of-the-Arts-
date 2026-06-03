import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import authService from '../services/authService';
import apiService from '../services/apiService';

const DashboardPage = () => {
  const [user, setUser] = useState(null);
  const [stats, setStats] = useState({ courses: 0, classes: 0, progress: 0 });
  const navigate = useNavigate();

  useEffect(() => {
    const currentUser = authService.getCurrentUser();
    if (!currentUser) {
      navigate('/login');
      return;
    }
    setUser(currentUser);
    fetchStats();
  }, [navigate]);

  const fetchStats = async () => {
    try {
      const enrollments = await apiService.get('/api/v1/enrollments');
      setStats({
        courses: enrollments.length,
        classes: 0,
        progress: 45,
      });
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  if (!user) return <div>Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-indigo-600">Dashboard</h1>
          <button
            onClick={handleLogout}
            className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
          >
            Logout
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Profile Card */}
        <div className="bg-gradient-to-r from-indigo-600 to-cyan-500 rounded-lg shadow-lg p-8 text-white mb-8">
          <div className="flex items-center">
            <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center mr-6">
              <span className="text-4xl text-indigo-600">
                {user.first_name?.[0] || 'U'}
              </span>
            </div>
            <div>
              <h2 className="text-3xl font-bold">
                {user.first_name} {user.last_name}
              </h2>
              <p className="text-indigo-100">{user.email}</p>
              <p className="text-indigo-100 capitalize">Role: {user.role}</p>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-4xl font-bold text-indigo-600">{stats.courses}</div>
            <p className="text-gray-600 mt-2">Courses Enrolled</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-4xl font-bold text-cyan-500">{stats.classes}</div>
            <p className="text-gray-600 mt-2">Live Classes</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-4xl font-bold text-green-500">{stats.progress}%</div>
            <p className="text-gray-600 mt-2">Overall Progress</p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button
            onClick={() => navigate('/courses')}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 px-6 rounded-lg transition"
          >
            📚 Courses
          </button>
          <button
            onClick={() => navigate('/classes')}
            className="bg-cyan-500 hover:bg-cyan-600 text-white font-bold py-4 px-6 rounded-lg transition"
          >
            🎥 Classes
          </button>
          <button
            onClick={() => navigate('/ai-tutor')}
            className="bg-pink-500 hover:bg-pink-600 text-white font-bold py-4 px-6 rounded-lg transition"
          >
            🤖 AI Tutor
          </button>
          <button
            onClick={() => navigate('/profile')}
            className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-4 px-6 rounded-lg transition"
          >
            👤 Profile
          </button>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;

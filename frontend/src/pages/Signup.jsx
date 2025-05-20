import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Signup = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
      const res = await axios.post('/api/auth/signup', { email, password });
      localStorage.setItem('token', res.data.access_token);
      navigate('/chat'); // Redirect after signup
    } catch (err) {
      setError(err.response?.data?.detail || 'Signup failed.');
    }
  };

  return (
    <div className="max-w-sm mx-auto mt-12 bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-bold mb-4">Create Account</h2>
      {error && <div className="text-red-600 mb-2">{error}</div>}
      <input
        type="email"
        placeholder="Email"
        className="w-full mb-3 p-2 border rounded"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        className="w-full mb-3 p-2 border rounded"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button
        onClick={handleSignup}
        className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
      >
        Sign Up
      </button>
    </div>
  );
};

export default Signup;

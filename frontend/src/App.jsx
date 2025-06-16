import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from './pages/Login';
import Signup from './pages/Signup';
import Chat from './pages/Chat';
import PrivateRoute from "./components/PrivateRoute";
import NavBar from './components/NavBar';
import Home from './pages/Home';
import SemanticSearch from './pages/SemanticSearch';
import News from './pages/News'; // ✅ Importing the News page
import NewsArchive from './pages/NewsArchive';

function App() {
  return (
    <BrowserRouter>
      <NavBar /> {/* ✅ Add NavBar at the top */}
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route 
          path="/chat" 
          element={
            <PrivateRoute>
              <Chat />
            </PrivateRoute>
          } 
        />
        {/* catch-all */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
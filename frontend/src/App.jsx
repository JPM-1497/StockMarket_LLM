import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import Home from './pages/Home';
import Chat from './pages/Chat';
import SemanticSearch from './pages/SemanticSearch';

const App = () => {
  return (
    <Router>
      <NavBar />
      <div className="p-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/semantic-search" element={<SemanticSearch />} />
          {/* Future routes */}
        </Routes>
      </div>
    </Router>
  );
};

export default App;

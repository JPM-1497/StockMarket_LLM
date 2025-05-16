import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import Home from './pages/Home';
import Chat from './pages/Chat';
import SemanticSearch from './pages/SemanticSearch';
import News from './pages/News'; // ✅ Importing the News page
import NewsArchive from './pages/NewsArchive';


const App = () => {
  return (
    <Router>
      <NavBar />
      <div className="p-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/semantic-search" element={<SemanticSearch />} />
          <Route path="/news" element={<News />} />
          <Route path="/news-archive" element={<NewsArchive />} />
          {/* Future routes */}
        </Routes>
      </div>
    </Router>
  );
};

export default App;

import React, { useState } from 'react';
import axios from 'axios';

const News = () => {
  const [keyword, setKeyword] = useState('');
  const [articles, setArticles] = useState([]);

  const fetchNews = async () => {
    if (!keyword) return;
    try {
      const res = await axios.get(`/api/news?keyword=${keyword}`);
      setArticles(res.data);
    } catch (error) {
      console.error("Failed to fetch news:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded shadow-lg">
        <h2 className="text-2xl font-bold mb-4 text-blue-700">📰 News Headlines</h2>
        <div className="flex gap-3 mb-6">
          <input
            type="text"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            placeholder="Search company or keyword..."
            className="flex-1 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            onClick={fetchNews}
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
          >
            Search
          </button>
        </div>

        <div className="space-y-4">
          {articles.map((a, idx) => (
            <div key={idx} className="p-4 border rounded bg-gray-100">
              <h3 className="text-lg font-semibold text-blue-800">
                <a href={a.url} target="_blank" rel="noopener noreferrer">
                  {a.title}
                </a>
              </h3>
              <p className="text-gray-700 mt-1">{a.description}</p>
              <p className="text-sm text-gray-500 mt-2">
                {a.source} | {a.published_at?.split('T')[0]}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default News;

// frontend/src/pages/SemanticSearch.jsx
import React, { useState } from 'react';
import axios from 'axios';

const SemanticSearch = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;

    try {
      const response = await axios.get(`/api/semantic_sector_search`, {
        params: { query }
      });

      console.log("API response:", response.data); // ✅ Debugging
      setResults(response.data.matches || []);
      setHasSearched(true);
    } catch (error) {
      console.error("Search failed:", error);
      setResults([]);
      setHasSearched(true);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-white to-blue-50 p-8">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-lg">
        <h1 className="text-2xl font-bold text-blue-700 mb-4 text-center">🔍 Semantic Sector Search</h1>

        <div className="flex gap-3 mb-6">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Try something like 'AI companies' or 'semiconductor industry'"
            className="flex-1 p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSearch}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Search
          </button>
        </div>

        {hasSearched && results.length === 0 && (
          <div className="text-center text-gray-500 mt-4">
            No matching stocks found. Try another query like "tech sector" or "AI".
          </div>
        )}

        <div className="space-y-4">
          {results.map((stock, idx) => (
            <div key={idx} className="p-4 border rounded shadow-sm bg-gray-50">
              <h2 className="text-lg font-semibold text-blue-700">
                {stock.symbol} — {stock.name}
              </h2>
              <p className="text-gray-700 mt-2">{stock.summary}</p>
              <p className="text-sm text-right text-gray-500 mt-1">
                Score: {stock.score !== undefined ? stock.score.toFixed(4) : "N/A"}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SemanticSearch;

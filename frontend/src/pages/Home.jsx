import React, { useState } from 'react';
import axios from 'axios';

function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!query.trim()) return;

    try {
      const response = await axios.get(`/api/search`, {
        params: { query }
      });

      setResults(response.data.matches || []);
      setError('');
    } catch (err) {
      console.error('Search failed:', err);
      setError('Something went wrong while fetching results.');
      setResults([]);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-3xl mx-auto bg-white p-6 rounded shadow-md">
        <h1 className="text-3xl font-bold mb-4 text-center text-blue-700">Stock Summary Search</h1>

        <div className="flex gap-2 mb-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter a company or topic..."
            className="flex-1 p-3 border border-gray-300 rounded"
          />
          <button
            onClick={handleSearch}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
          >
            Search
          </button>
        </div>

        {error && <div className="text-red-600 mb-4">{error}</div>}

        {results.length > 0 && (
          <div className="space-y-4">
            {results.map((item, idx) => (
              <div key={idx} className="p-4 border rounded bg-gray-50 shadow-sm">
                <h2 className="text-xl font-semibold text-blue-800">{item.symbol} — {item.name}</h2>
                <p className="text-gray-700 mt-2" dangerouslySetInnerHTML={{ __html: item.summary }}></p>
                <div className="text-sm text-gray-500 mt-2 text-right">Relevance: {item.score}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Home;

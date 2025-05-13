// src/components/SearchPanel.jsx
import React, { useState } from 'react';

export default function SearchPanel() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    if (!query.trim()) return;

    const res = await fetch(`/api/search?query=${encodeURIComponent(query)}`);
    const data = await res.json();
    setResults(data.matches || []);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search stock summaries..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: '300px', marginRight: '1rem' }}
      />
      <button onClick={handleSearch}>Search</button>

      <ul style={{ marginTop: '2rem' }}>
        {results.map((item) => (
          <li key={item.symbol} style={{ marginBottom: '1rem' }}>
            <strong>{item.symbol} - {item.name}</strong>
            <p dangerouslySetInnerHTML={{ __html: item.summary }} />
            <small>Score: {item.score}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}

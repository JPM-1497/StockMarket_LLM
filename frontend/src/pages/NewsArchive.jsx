import React, { useEffect, useState } from 'react';
import axios from 'axios';

const NewsArchive = () => {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    axios.get('/api/news?keyword=')
      .then(res => setArticles(res.data))
      .catch(err => console.error("Error fetching news:", err));
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto bg-white p-6 rounded-lg shadow-lg">
        <h1 className="text-2xl font-bold text-blue-700 mb-6 text-center">📰 News Archive</h1>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm text-left text-gray-700">
            <thead className="bg-blue-100 text-xs uppercase text-blue-700">
              <tr>
                <th className="px-4 py-2">Title</th>
                <th className="px-4 py-2">Description</th>
                <th className="px-4 py-2">Source</th>
                <th className="px-4 py-2">Published</th>
                <th className="px-4 py-2">Link</th>
              </tr>
            </thead>
            <tbody>
              {articles.map((a, idx) => (
                <tr key={idx} className="border-t border-gray-200 hover:bg-gray-50">
                  <td className="px-4 py-2 font-medium">{a.title}</td>
                  <td className="px-4 py-2">{a.description?.slice(0, 100)}...</td>
                  <td className="px-4 py-2">{a.source}</td>
                  <td className="px-4 py-2">{new Date(a.published_at).toLocaleString()}</td>
                  <td className="px-4 py-2">
                    <a href={a.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">
                      View
                    </a>
                  </td>
                </tr>
              ))}
              {articles.length === 0 && (
                <tr>
                  <td colSpan="5" className="px-4 py-4 text-center text-gray-500">No news articles found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default NewsArchive;

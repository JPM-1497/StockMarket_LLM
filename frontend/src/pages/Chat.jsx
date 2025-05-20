import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const Chat = () => {
  const [messages, setMessages] = useState([
    { role: 'system', content: 'Ask me about any stock, sector, or trend.' }
  ]);
  const [input, setInput] = useState('');
  const [newsResults, setNewsResults] = useState([]);
  const [results, setResults] = useState({});
  const [matchedTickers, setMatchedTickers] = useState([]);
  const [submitted, setSubmitted] = useState(false);
  const [expandedCard, setExpandedCard] = useState(null);
  const chatContainerRef = useRef(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');
    setSubmitted(true);

    try {
      const response = await axios.get('/api/compare_stocks', {
        params: { query: input }
      });

      const summary = response.data.summary || '';
      const resultsObj = response.data.results || {};

      // Filter: match based on summary text (ticker or name)
      const filteredTickers = Object.entries(resultsObj)
      .filter(([symbol, data]) => {
        const regexSymbol = new RegExp(`\\b${symbol}\\b`, 'i');
        const allNameWords = data.name.split(/\s+/).filter(w => w.length > 2); // Skip short/common words
        const nameMatched = allNameWords.some(word => {
          const nameRegex = new RegExp(`\\b${word}\\b`, 'i');
          return nameRegex.test(summary);
        });
        return regexSymbol.test(summary) || nameMatched;
      })
      .map(([symbol]) => symbol);
    

      // Highlight tickers in the summary
      let highlightedSummary = summary;
      filteredTickers.forEach(ticker => {
        const regex = new RegExp(`\\b${ticker}\\b`, 'gi');
        highlightedSummary = highlightedSummary.replace(
          regex,
          match => `<strong class="text-blue-700">${match}</strong>`
        );
      });

      setMessages([...newMessages, { role: 'assistant', content: highlightedSummary }]);
      setResults(resultsObj);
      setMatchedTickers(filteredTickers);

      const topTicker = filteredTickers[0];
      if (topTicker) {
        const newsRes = await axios.get('/api/news', {
          params: { keyword: topTicker }
        });
        setNewsResults(newsRes.data);
      }

    } catch (error) {
      setMessages([...newMessages, { role: 'assistant', content: '❌ Something went wrong.' }]);
      setNewsResults([]);
    }
  };

  useEffect(() => {
    chatContainerRef.current?.scrollTo({
      top: chatContainerRef.current.scrollHeight,
      behavior: 'smooth',
    });
  }, [messages]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-white to-blue-50 p-4">
      {submitted ? (
        <div className="flex gap-4">
          {/* Chat Panel */}
          <div className="w-2/5 bg-white rounded-lg shadow-lg flex flex-col h-[85vh]">
            <div className="bg-blue-700 text-white text-lg px-4 py-2 rounded-t-lg font-semibold">
              💬 Stock Copilot
            </div>
            <div ref={chatContainerRef} className="flex-1 overflow-y-auto px-4 py-3 space-y-2">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`whitespace-pre-wrap p-2 rounded-md ${
                    msg.role === 'user'
                      ? 'bg-blue-100 text-right'
                      : msg.role === 'assistant'
                      ? 'bg-gray-100 text-left'
                      : 'text-sm text-gray-500 text-center'
                  }`}
                  dangerouslySetInnerHTML={{ __html: msg.content }}
                />
              ))}
            </div>
            <div className="px-4 py-3 border-t bg-white flex gap-2">
              <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && sendMessage()}
                placeholder="Ask more about stock trends..."
                className="flex-1 p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
              <button
                onClick={sendMessage}
                className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700"
              >
                Send
              </button>
            </div>
          </div>

          {/* Right Panel */}
          <div className="w-3/5 space-y-6">
            {/* KPI Cards */}
            {matchedTickers.length > 0 && (
              <div>
                <h2 className="text-lg font-semibold text-blue-700 mb-2">📊 Matched Stocks</h2>
                <div className="grid grid-cols-2 gap-4">
                  {matchedTickers.map((symbol) => {
                    const data = results[symbol];
                    if (!data) return null;
                    return (
                      <div key={symbol} className="bg-white p-4 rounded-lg shadow border border-gray-200">
                        <div className="text-sm text-gray-500 mb-1">{data.name}</div>
                        <div className="text-2xl font-bold text-blue-700">{symbol}</div>
                        <div
                          className={`text-sm font-semibold mt-1 ${
                            data.pct_change >= 0 ? 'text-green-600' : 'text-red-600'
                          }`}
                        >
                          {data.pct_change >= 0 ? '+' : ''}
                          {data.pct_change}%
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* News */}
            <div>
              <h2 className="text-xl font-bold text-blue-700 mb-4">📰 Related News</h2>
              {newsResults.length > 0 ? (
                <div className="grid grid-cols-1 gap-4">
                  {newsResults.map((article, idx) => {
                    const isExpanded = expandedCard === idx;
                    return (
                      <div key={idx} className="bg-white p-4 rounded-lg shadow overflow-hidden transition-all">
                        <a
                          href={article.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 font-semibold hover:underline block mb-1"
                        >
                          {article.title}
                        </a>
                        <p className={`text-gray-700 text-sm ${isExpanded ? '' : 'line-clamp-3'}`}>
                          {article.description || 'No description available.'}
                        </p>
                        <div className="text-xs text-gray-400 mt-2">{article.published_at}</div>
                        <button
                          onClick={() => setExpandedCard(isExpanded ? null : idx)}
                          className="text-sm text-blue-500 mt-2 hover:underline"
                        >
                          {isExpanded ? 'Show Less' : 'Read More'}
                        </button>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <p className="text-gray-500">No news articles found yet.</p>
              )}
            </div>
          </div>
        </div>
      ) : (
        // Initial Layout
        <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow-xl flex flex-col h-[85vh]">
          <div className="text-xl font-bold text-blue-800 mb-4">💬 Stock Copilot</div>
          <div ref={chatContainerRef} className="flex-1 overflow-y-auto space-y-3">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`whitespace-pre-wrap p-3 rounded ${
                  msg.role === 'user'
                    ? 'bg-blue-100 text-right'
                    : msg.role === 'assistant'
                    ? 'bg-gray-100 text-left'
                    : 'text-sm text-center text-gray-400'
                }`}
              >
                {msg.content}
              </div>
            ))}
          </div>
          <div className="mt-4 flex gap-2">
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && sendMessage()}
              placeholder="Ask about Meta vs Amazon in 2025..."
              className="flex-1 p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
            <button
              onClick={sendMessage}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chat;

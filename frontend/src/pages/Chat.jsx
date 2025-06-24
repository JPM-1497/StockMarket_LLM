import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  Legend,
  CategoryScale,
  TimeScale,
} from 'chart.js';
import 'chartjs-adapter-date-fns';

ChartJS.register(LineElement, PointElement, LinearScale, Title, Tooltip, Legend, CategoryScale, TimeScale);

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
  const [activeTab, setActiveTab] = useState('chart');
  const chatContainerRef = useRef(null);

  const token = localStorage.getItem("token");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');
    setSubmitted(true);

    try {
      const response = await axios.get('/api/compare_stocks', {
        params: { query: input },
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      let summary = '';
      let resultsObj = {};

      if (typeof response.data === 'string') {
        summary = response.data;
      } else {
        summary = response.data?.summary || '';
        resultsObj = response.data?.results || {};
      }

      const filteredTickers = Object.keys(resultsObj);

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
          params: { keyword: topTicker },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setNewsResults(newsRes.data);
      }

    } catch (error) {
      console.error('❌ API Error:', error);
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

  // ✅ UPDATED renderLineChart with unique colors & bigger size
  const renderLineChart = () => {
    if (!matchedTickers.length || !results || !results[matchedTickers[0]]?.daily) {
      return <p>No chart data available.</p>;
    }

    const colors = [
      '#1f77b4', // blue
      '#ff7f0e', // orange
      '#2ca02c', // green
      '#d62728', // red
      '#9467bd', // purple
      '#8c564b', // brown
      '#e377c2', // pink
      '#7f7f7f', // gray
      '#bcbd22', // olive
      '#17becf'  // cyan
    ];

    const datasets = matchedTickers.map((ticker, index) => {
      const prices = results[ticker]?.daily;
      if (!Array.isArray(prices)) return null;

      const color = colors[index % colors.length];

      return {
        label: ticker,
        data: prices.map(p => ({
          x: new Date(p.date),
          y: p.close
        })),
        borderWidth: 2,
        borderColor: color,
        backgroundColor: color + '33',
        tension: 0.4,
      };
    }).filter(Boolean);

    const data = { datasets };

    const options = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          type: 'time',
          time: { unit: 'day' },
          title: { display: true, text: 'Date' }
        },
        y: {
          title: { display: true, text: 'Close Price ($)' }
        }
      },
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: 'Stock Price Over Time' },
        tooltip: {
          callbacks: {
            label: (context) => `$${context.parsed.y.toFixed(2)}`
          }
        }
      }
    };

    return (
      <div className="h-[500px]">
        <Line data={data} options={options} />
      </div>
    );
  };

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
                placeholder="Ask more about stock trends."
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
                <h2 className="text-base font-semibold text-blue-700 mb-2">📊 Matched Stocks</h2>
                <div className="grid grid-cols-3 gap-3">
                  {matchedTickers.map((symbol) => {
                    const data = results[symbol];
                    if (!data) return null;
                    return (
                      <div 
                        key={symbol} 
                        className="bg-white p-3 rounded shadow border border-gray-200 text-sm"
                      >
                        <div className="text-xs text-gray-500">{data.name}</div>
                        <div className="text-lg font-bold text-blue-700">{symbol}</div>
                        <div className="mt-1">
                          <div>Start: ${data.start_price?.toFixed(2)}</div>
                          <div>End: ${data.end_price?.toFixed(2)}</div>
                          <div className={data.pct_change >= 0 ? 'text-green-600' : 'text-red-600'}>
                            Change: {data.pct_change >= 0 ? '+' : ''}
                            {data.pct_change?.toFixed(2)}%
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Tabs */}
            <div className="flex gap-4 mt-4">
              <button
                onClick={() => setActiveTab('chart')}
                className={`px-4 py-2 rounded-t-lg font-semibold ${
                  activeTab === 'chart' ? 'bg-blue-200 text-blue-800' : 'bg-gray-100 text-gray-500'
                }`}
              >
                📈 Line Chart
              </button>
              <button
                onClick={() => setActiveTab('news')}
                className={`px-4 py-2 rounded-t-lg font-semibold ${
                  activeTab === 'news' ? 'bg-blue-200 text-blue-800' : 'bg-gray-100 text-gray-500'
                }`}
              >
                📰 News
              </button>
            </div>

            <div className="bg-white p-4 rounded-lg shadow">
              {activeTab === 'chart' ? (
                matchedTickers.length > 0 ? renderLineChart() : <p>No chart data available.</p>
              ) : (
                <div>
                  {newsResults.length > 0 ? (
                    <div className="grid grid-cols-1 gap-4">
                      {newsResults.map((article, idx) => {
                        const isExpanded = expandedCard === idx;
                        return (
                          <div key={idx} className="bg-white p-4 rounded-lg shadow">
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
              placeholder="Ask about Meta vs Amazon in 2025."
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

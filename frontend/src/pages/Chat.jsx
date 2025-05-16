// frontend/src/pages/CompareChat.jsx
import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const CompareChat = () => {
  const [messages, setMessages] = useState([
    { role: 'system', content: "Ask about stock comparisons like: 'Compare Google and Tesla in 2023'" }
  ]);
  const [input, setInput] = useState('');
  const chatRef = useRef(null);

  const sendQuery = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput('');

    try {
      const response = await axios.get('/api/compare_stocks', {
        params: { query: input }
      });

      const { summary, results } = response.data;
      const tickersSummary = Object.entries(results).map(([symbol, data]) => {
        return `${symbol}: ${data.pct_change.toFixed(2)}%`;
      }).join(', ');

      const assistantMessage = {
        role: 'assistant',
        content: `${summary}\n\n${tickersSummary}`
      };
      setMessages([...updatedMessages, assistantMessage]);
    } catch (err) {
      setMessages([...updatedMessages, {
        role: 'assistant',
        content: "❌ Error fetching comparison."
      }]);
    }
  };

  useEffect(() => {
    chatRef.current?.scrollTo({ top: chatRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 to-blue-50 p-6">
      <div className="max-w-3xl mx-auto bg-white rounded-lg shadow-lg h-[85vh] flex flex-col">
        <div className="px-6 py-4 bg-blue-700 text-white text-lg font-semibold rounded-t-lg">
          📈 Stock Comparison Chat
        </div>

        <div ref={chatRef} className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`whitespace-pre-wrap p-3 rounded-lg max-w-[80%] ${
                msg.role === 'user' ? 'bg-blue-100 self-end text-right' :
                msg.role === 'assistant' ? 'bg-gray-200 self-start text-left' :
                'text-sm text-gray-500 text-center'
              }`}
            >
              {msg.content}
            </div>
          ))}
        </div>

        <div className="p-4 bg-white border-t flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendQuery()}
            placeholder="Try: Compare Meta and Amazon in 2025"
            className="flex-1 p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={sendQuery}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default CompareChat;

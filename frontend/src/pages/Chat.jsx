import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const Chat = () => {
  const [messages, setMessages] = useState([
    { role: 'system', content: 'Ask me about any stock, sector, or trend.' }
  ]);
  const [input, setInput] = useState('');
  const chatContainerRef = useRef(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');

    try {
      const response = await axios.post('/api/chat', {
        messages: newMessages.slice(-6) // send last few messages for context
      });

      setMessages([...newMessages, { role: 'assistant', content: response.data.response }]);
    } catch (error) {
      setMessages([...newMessages, { role: 'assistant', content: '❌ Something went wrong.' }]);
    }
  };

  useEffect(() => {
    chatContainerRef.current?.scrollTo({
      top: chatContainerRef.current.scrollHeight,
      behavior: 'smooth',
    });
  }, [messages]);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center px-4">
      <div className="w-full max-w-3xl bg-white shadow-lg rounded-lg flex flex-col h-[85vh]">
        <div className="bg-blue-600 text-white text-xl font-semibold px-6 py-4 rounded-t-lg">
          💬 Stock Market Assistant
        </div>

        <div
          ref={chatContainerRef}
          className="flex-1 overflow-y-auto px-6 py-4 space-y-4 bg-gray-50"
        >
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`whitespace-pre-wrap px-4 py-2 rounded-lg w-fit max-w-[80%] ${
                msg.role === 'user'
                  ? 'bg-blue-100 self-end text-right'
                  : msg.role === 'system'
                  ? 'text-sm text-gray-500'
                  : 'bg-gray-200 self-start'
              }`}
            >
              {msg.content}
            </div>
          ))}
        </div>

        <div className="px-6 py-4 border-t flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask a question like 'Compare Tesla and Ford stock performance...'"
            className="flex-1 p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            onClick={sendMessage}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;

import React, { useState } from 'react';
import './styles.css';

const languageOptions = {
  english: 'en',
  hindi: 'hi',
  bengali: 'bn',
  telugu: 'te',
  marathi: 'mr',
  tamil: 'ta',
  urdu: 'ur',
  gujarati: 'gu',
  kannada: 'kn',
  malayalam: 'ml',
  punjabi: 'pa'
};

function App() {
  const [message, setMessage] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [language, setLanguage] = useState('en');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    setChatLog([...chatLog, { sender: 'user', text: message }]);
    setLoading(true);

    const response = await fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, language })
    });

    const data = await response.json();
    setChatLog(prev => [...prev, { sender: 'bot', text: data.response }]);
    setMessage('');
    setLoading(false);
  };

  return (
    <div className="chat-container">
      <h2>Agricultural ChatBot Assistant</h2>

      <select
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
        className="language-select"
      >
        {Object.entries(languageOptions).map(([lang, code]) => (
          <option key={code} value={code}>{lang}</option>
        ))}
      </select>

      <div className="chat-box">
        {chatLog.map((chat, index) => (
          <div key={index} className={chat.sender === 'user' ? 'user-message' : 'bot-message'}>
            {chat.text}
          </div>
        ))}
        {loading && <div className="bot-message">Typing...</div>}
      </div>

      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask me about crops, ROI, etc."
        onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
      />
      <button onClick={sendMessage} disabled={loading}>Send</button>
    </div>
  );
}

export default App;

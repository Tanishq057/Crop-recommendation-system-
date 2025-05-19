import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [supportedLanguages, setSupportedLanguages] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch supported languages when component mounts
    axios.get('http://localhost:5000/support-languages')
      .then(response => {
        setSupportedLanguages(response.data.languages);
      })
      .catch(error => {
        console.error('Error fetching languages:', error);
      });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (message.trim() === '') return;
    
    // Add user message to chat history
    setChatHistory([...chatHistory, { sender: 'user', text: message }]);
    
    setLoading(true);
    
    try {
      // Send message to backend
      const response = await axios.post('http://localhost:5000/chat', {
        message: message,
        language: selectedLanguage
      });
      
      // Add bot response to chat history
      setChatHistory(prevHistory => [
        ...prevHistory, 
        { sender: 'bot', text: response.data.response }
      ]);
    } catch (error) {
      console.error('Error communicating with backend:', error);
      
      // Add error message to chat history
      setChatHistory(prevHistory => [
        ...prevHistory, 
        { sender: 'bot', text: 'Sorry, I encountered an error. Please try again.' }
      ]);
    } finally {
      setLoading(false);
      setMessage('');
    }
  };

  return (
    <div className="app-container">
      <div className="chat-container">
        <div className="header">
          <h1>Agricultural Assistant</h1>
          <select 
            value={selectedLanguage} 
            onChange={(e) => setSelectedLanguage(e.target.value)}
          >
            {supportedLanguages.map(lang => (
              <option key={lang.code} value={lang.code}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>
        
        <div className="chat-messages">
          {chatHistory.map((chat, index) => (
            <div key={index} className={`message ${chat.sender}`}>
              {chat.text}
            </div>
          ))}
          {loading && <div className="loading">Bot is typing...</div>}
        </div>
        
        <form onSubmit={handleSubmit} className="input-form">
          <input 
            type="text" 
            value={message} 
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Enter your message..."
          />
          <button type="submit" disabled={loading}>Send</button>
        </form>
      </div>
    </div>
  );
}

export default App;
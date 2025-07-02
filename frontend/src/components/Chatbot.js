import React, { useState } from 'react';
import axios from 'axios';
import './Chatbot.css';



const Chatbot = () => {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleQuery = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:5050/api/chatbotexpress', { query }); 
      setAnswer(res.data.answer || 'No answer received');
    } catch (err) {
      setAnswer('Error: ' + err.message);
    }
    setLoading(false);
  };

  return (
    <div className="wholecontainer">




      <h2>IITG Chatbot</h2>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question..."
       
      />
      <button onClick={handleQuery} style={{ marginLeft: '1rem', padding: '8px' }}>
        Ask
      </button>
      <div >
        {loading ? <p>Loading...</p> : <p><strong>Answer:</strong> {answer}</p>}
      </div>
    </div>
  );
};

export default Chatbot;

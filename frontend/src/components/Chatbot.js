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




      <div className="header">IITG Chatbot</div>
    
     
      <div >
        {loading ? <p>Loading...</p> : <p><strong>Answer:</strong> {answer}</p>}
      </div>
     <div className="inputandbutton">  
      
      <div className="inputbox"><input 
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question..."
      />
      </div>
      
      
      <div className="button">
        <button onClick={handleQuery}  >
         ASK
        </button>
      
      </div> 
      
      
      </div>
      


    </div>
  );
};

export default Chatbot;

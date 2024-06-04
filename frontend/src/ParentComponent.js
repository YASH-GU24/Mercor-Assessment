import React, { useState } from 'react';
import Chat from './Chat';
import Results from './Results';
import './App.css';
import './ParentComponent.css';

function ParentComponent() {
  const [chatHistory, setChatHistory] = useState([]);
  const [results, setResults] = useState([]);

  const sendChatToAPI = (chatHistory,result) => {
    // Simulated API call; replace with your API endpoint
    console.log('Sending chat to API:', chatHistory);
    console.log(result);
    setResults(result);

    // Simulated API response; replace with your API logic
  };

  return (
    <>
    <div className="parent-container">
      <div className="chat">
        <Chat onChatSubmit={sendChatToAPI} />
      </div>
      <div className="results">
        <Results results={results} />
      </div>
    </div>
    </>
  );
}

export default ParentComponent;

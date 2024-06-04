import React, { useState, useEffect } from 'react';
import './Chat.css';
import SendIcon from '@mui/icons-material/Send';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';

const Chat = ({ onChatSubmit }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [listening, setListening] = useState(false);
  const { transcript, browserSupportsSpeechRecognition,resetTranscript } = useSpeechRecognition();

  const handleUserMessage = () => {
    if (newMessage.trim() === '') return;

    const userMessage = `${newMessage}`;
    const updatedMessages = [...messages, { text: userMessage, type: 'user' }];
    setMessages(updatedMessages);

    // Clear the input field
 
    resetTranscript();
    
 
    setNewMessage('');
    // Call the API for a response
    callAPI(updatedMessages, newMessage);
  };

  const startListening = () => {
    if (listening) {
      SpeechRecognition.stopListening();
    } else {
      SpeechRecognition.startListening({ continuous: true, language: 'en-IN' });
    }
    setListening(!listening);
  };


  useEffect(() => {
    console.log(transcript);
    if (transcript) {
      setNewMessage(transcript);
    }
   
  }, [transcript]);

  if (!browserSupportsSpeechRecognition) {
    return null;
  }

  const callAPI = (chatHistory, userMessage) => {
    fetch('http://localhost:5000/get_candidates', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ chatHistory }),
    })
      .then((response) => response.json())
      .then((data) => {
        const aiReply = `AI: ${data.answer}`;

        // Update the chat with both the AI reply and user message
        const updatedMessages = [
          ...chatHistory,
          { text: aiReply, type: 'ai' },
        ];

        setMessages(updatedMessages);

        // Send the entire chat history to the parent component
        onChatSubmit(updatedMessages, data.results);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  return (
    <div className="chat-container">
      <h2 className="chat-heading">Search Candidates</h2>

      <div className="chat-messages">
        {messages.map((message, index) => (
          <div
            key={index}
            className={message.type === 'user' ? 'user-message' : 'ai-message'}
          >
            {message.text}
          </div>
        ))}
      </div>
      <div className="chat-input">
      <button onClick={startListening} className="mic-btn">
          {listening ?  <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0z" fill="none"/><path d="M12 14c1.66 0 2.99-1.34 2.99-3L15 5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z"/></svg> : <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0zm0 0h24v24H0z" fill="none"/><path d="M19 11h-1.7c0 .74-.16 1.43-.43 2.05l1.23 1.23c.56-.98.9-2.09.9-3.28zm-4.02.17c0-.06.02-.11.02-.17V5c0-1.66-1.34-3-3-3S9 3.34 9 5v.18l5.98 5.99zM4.27 3L3 4.27l6.01 6.01V11c0 1.66 1.33 3 2.99 3 .22 0 .44-.03.65-.08l1.66 1.66c-.71.33-1.5.52-2.31.52-2.76 0-5.3-2.1-5.3-5.1H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c.91-.13 1.77-.45 2.54-.9L19.73 21 21 19.73 4.27 3z"/></svg>}
        </button>
        <input
          type="text"
          placeholder="Type a message..."
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
        />
        <button onClick={handleUserMessage} className="sendbtn">
          <SendIcon />
        </button>
     
      </div>
    </div>
  );
};

export default Chat;

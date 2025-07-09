import React, { useState } from 'react';
import { useSpeechRecognition, useSpeechSynthesis } from 'react-speech-kit';
import axios from 'axios';

const VoiceAssistant = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [isListening, setIsListening] = useState(false);
  
  const { listen, stop } = useSpeechRecognition({
    onResult: (result) => setQuery(result),
    onEnd: () => setIsListening(false)
  });
  
  const { speak } = useSpeechSynthesis();
  
  const handleListen = () => {
    setIsListening(true);
    listen();
  };
  
  const handleSubmit = async () => {
    try {
      const res = await axios.post(
        process.env.REACT_APP_API_URL + '/api/query',
        { query },
        {
          headers: {
            'X-User-ID': 'current-user-id', // Replace with actual user ID
            'Content-Type': 'application/json'
          }
        }
      );
      
      setResponse(res.data.text);
      speak({ text: res.data.text });
      
      // Display recommendations
      if (res.data.items) {
        console.log('Recommendations:', res.data.items);
      }
    } catch (error) {
      console.error('Error:', error);
      setResponse('Sorry, there was an error processing your request.');
    }
  };
  
  return (
    <div className="voice-assistant">
      <button 
        onMouseDown={handleListen}
        onMouseUp={stop}
        className={isListening ? 'listening' : ''}
      >
        {isListening ? 'Listening...' : 'Hold to Speak'}
      </button>
      
      <div className="query-display">
        <p>You asked: {query}</p>
      </div>
      
      <button onClick={handleSubmit} disabled={!query}>
        Get Recommendations
      </button>
      
      <div className="response">
        <p>Assistant says: {response}</p>
      </div>
    </div>
  );
};

export default VoiceAssistant;

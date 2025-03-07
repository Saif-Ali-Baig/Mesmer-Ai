import React, { useState, useEffect } from 'react';
import MicButton from './components/MicButton';
import AudioPlayer from './components/AudioPlayer';
import Login from './components/Login';
import { connectWebSocket } from './api/websocket';
import './styles/main.css';

function App() {
  const [mode, setMode] = useState('friend');
  const [token, setToken] = useState(null);
  const [ws, setWs] = useState(null);
  const [responseAudio, setResponseAudio] = useState(null);

  useEffect(() => {
    if (token) {
      const websocket = connectWebSocket(token, setResponseAudio);
      setWs(websocket);
      return () => websocket.close();
    }
  }, [token]);

  if (!token) return <Login setToken={setToken} />;

  return (
    <div className="app-container">
      <h1>Your Voice Companion</h1>
      <button 
        onClick={() => {
          const newMode = mode === 'friend' ? 'therapist' : 'friend';
          setMode(newMode);
          if (ws) ws.send(`switch:${newMode}`);
        }}
        className="mode-button"
      >
        Switch to {mode === 'friend' ? 'Therapist' : 'Friend'}
      </button>
      <MicButton ws={ws} />
      <AudioPlayer audioData={responseAudio} />
    </div>
  );
}

export default App;
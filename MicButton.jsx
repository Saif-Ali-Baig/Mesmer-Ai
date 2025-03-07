import React, { useState } from 'react';
import { ReactMic } from 'react-mic';

const MicButton = ({ ws }) => {
  const [recording, setRecording] = useState(false);

  const onData = (recordedBlob) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(recordedBlob.blob);
    }
  };

  return (
    <div>
      <button
        onClick={() => setRecording(!recording)}
        className="mic-button"
        aria-label={recording ? "Stop recording" : "Start recording"}
      >
        {recording ? "Stop" : "Talk to Me"}
      </button>
      <ReactMic
        record={recording}
        onData={onData}
        sampleRate={16000}
        mimeType="audio/webm"
      />
    </div>
  );
};

export default MicButton;
import React, { useEffect, useRef } from 'react';

const AudioPlayer = ({ audioData }) => {
  const audioRef = useRef(null);

  useEffect(() => {
    if (audioData) {
      const blob = new Blob([audioData], { type: 'audio/mp3' });
      audioRef.current.src = URL.createObjectURL(blob);
      audioRef.current.play();
    }
  }, [audioData]);

  return <audio ref={audioRef} controls hidden />;
};

export default AudioPlayer;
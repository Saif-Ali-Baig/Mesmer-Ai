export function connectWebSocket(token, setResponseAudio) {
  const ws = new WebSocket('ws://localhost:8080/ws', [], {
    headers: { 'Authorization': `Bearer ${token}` }
  });

  ws.onmessage = (event) => {
    if (typeof event.data === 'string') {
      console.log(event.data);
    } else {
      event.data.arrayBuffer().then(buffer => setResponseAudio(buffer));
    }
  };

  ws.onerror = (err) => console.error('WebSocket error:', err);
  return ws;
}
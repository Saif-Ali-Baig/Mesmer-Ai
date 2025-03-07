import axios from 'axios';

const api = axios.create({ baseURL: 'http://localhost:8080' });

export async function login(username, password) {
  try {
    const response = await api.post('/login', { username, password });
    return response.data.token;
  } catch (error) {
    console.error('Login failed:', error);
    return null;
  }
}
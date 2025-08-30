import axios from 'axios';
import { ChatRequest, ChatResponse, SlideTheme } from '@/types';

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  (typeof window !== 'undefined' ? window.location.origin : 'http://localhost:8001');

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatAPI = {
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post('/chat', request);
    return response.data;
  },

  getThemes: async (): Promise<{ themes: Record<string, SlideTheme> }> => {
    const response = await api.get('/themes');
    return response.data;
  },

  generateSlides: async (markdown: string, theme: string = 'professional') => {
    const response = await api.post('/generate-slides', {
      markdown,
      theme,
    });
    return response.data;
  },

  getStatus: async () => {
    const response = await api.get('/api/');
    return response.data;
  },

  getDemoContent: async () => {
    const response = await api.get('/demo');
    return response.data;
  },
};

export default api;

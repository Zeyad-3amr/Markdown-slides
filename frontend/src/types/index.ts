export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  slides_html?: string;
  theme_suggestion?: string;
}

export interface SlideTheme {
  name: string;
  primary_color: string;
  secondary_color: string;
  background: string;
  font_family: string;
  description: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  message: string;
  slides_html?: string;
  theme_suggestion?: string;
  conversation_id: string;
}

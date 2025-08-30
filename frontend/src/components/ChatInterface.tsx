'use client';

import { ChatMessage } from '@/types';
import { User, Bot, FileText } from 'lucide-react';

interface ChatInterfaceProps {
  messages: ChatMessage[];
  isLoading: boolean;
  messagesEndRef: React.RefObject<HTMLDivElement>;
}

export default function ChatInterface({
  messages,
  isLoading,
  messagesEndRef,
}: ChatInterfaceProps) {
  return (
    <div className="flex-1 overflow-y-auto overflow-x-hidden p-3 space-y-3 min-h-0 max-h-full">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex gap-3 ${
            message.role === 'user' ? 'justify-end' : 'justify-start'
          }`}
        >
          <div
            className={`flex gap-2 max-w-[80%] break-words ${
              message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
            }`}
          >
            <div
              className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-purple-600 text-white'
              }`}
            >
              {message.role === 'user' ? <User size={12} /> : <Bot size={12} />}
            </div>

            <div
              className={`rounded-lg px-3 py-1.5 break-words overflow-hidden ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white ml-auto'
                  : 'bg-gray-700 text-gray-100'
              }`}
            >
              <p className="whitespace-pre-wrap text-sm">{message.content}</p>

              {message.slides_html && (
                <div className="mt-1 pt-1 border-t border-gray-600">
                  <div className="flex items-center gap-1 text-xs text-green-600">
                    <FileText size={12} />
                    <span>Slides generated!</span>
                  </div>
                </div>
              )}

              {message.theme_suggestion && (
                <div className="mt-1 pt-1 border-t border-gray-600">
                  <p className="text-xs text-blue-600">{message.theme_suggestion}</p>
                </div>
              )}

              <div className="text-xs opacity-60 mt-0.5">
                {message.timestamp.toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </div>
            </div>
          </div>
        </div>
      ))}

      {isLoading && (
        <div className="flex gap-2">
          <div className="flex-shrink-0 w-6 h-6 rounded-full bg-purple-600 text-white flex items-center justify-center">
            <Bot size={12} />
          </div>
          <div className="bg-gray-700 rounded-lg px-3 py-1.5">
            <div className="flex items-center gap-2">
              <div className="flex space-x-1">
                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"></div>
                <div
                  className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"
                  style={{ animationDelay: '0.1s' }}
                ></div>
                <div
                  className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"
                  style={{ animationDelay: '0.2s' }}
                ></div>
              </div>
              <span className="text-gray-300 text-xs">Processing...</span>
            </div>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}

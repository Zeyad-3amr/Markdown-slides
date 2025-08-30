'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, FileText, Sparkles, Download, Palette } from 'lucide-react';
import toast from 'react-hot-toast';
import { chatAPI } from '@/lib/api';
import { ChatMessage, SlideTheme } from '@/types';
import ChatInterface from '@/components/ChatInterface';
import SlidePreview from '@/components/SlidePreview';
import ThemeSelector from '@/components/ThemeSelector';

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [currentSlides, setCurrentSlides] = useState<string | null>(null);
  const [themes, setThemes] = useState<Record<string, SlideTheme>>({});
  const [selectedTheme, setSelectedTheme] = useState('professional');
  const [showPreview, setShowPreview] = useState(false);
  const [apiStatus, setApiStatus] = useState<any>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Load themes and status on mount
    loadThemes();
    loadApiStatus();

    // Add welcome message
    setMessages([
      {
        id: '1',
        role: 'assistant',
        content:
          "Hi! I'm your Markdown-to-Slides Agent. 🎯 Paste your markdown content and I'll convert it into beautiful slides with AI-powered theme suggestions!",
        timestamp: new Date(),
      },
    ]);
  }, []);

  const loadThemes = async () => {
    try {
      const { themes } = await chatAPI.getThemes();
      setThemes(themes);
    } catch (error) {
      console.error('Failed to load themes:', error);
    }
  };

  const loadApiStatus = async () => {
    try {
      const status = await chatAPI.getStatus();
      setApiStatus(status);
      console.log('--------------------------------');
      console.log('API status:', status);
      console.log('--------------------------------');
    } catch (error) {
      console.error('Failed to load API status:', error);
    }
  };

  const loadDemoContent = async () => {
    try {
      const demo = await chatAPI.getDemoContent();
      setInputMessage(demo.markdown);
      toast.success('Demo content loaded! Click Send to generate slides.');
    } catch (error) {
      console.error('Failed to load demo content:', error);
      toast.error('Failed to load demo content.');
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setInputMessage('');

    try {
      const response = await chatAPI.sendMessage({
        message: inputMessage,
        conversation_id: conversationId ?? undefined,
      });

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.message,
        timestamp: new Date(),
        slides_html: response.slides_html,
        theme_suggestion: response.theme_suggestion,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setConversationId(response.conversation_id);

      if (response.slides_html) {
        setCurrentSlides(response.slides_html);
        setShowPreview(true);
        toast.success('Slides generated successfully! 🎉');
      }

      if (response.theme_suggestion) {
        toast.success(`Theme suggestion: ${response.theme_suggestion}`);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      toast.error('Failed to process your message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const regenerateWithTheme = async (themeKey: string) => {
    if (!currentSlides) return;

    const lastUserMessage = messages.filter((m) => m.role === 'user').pop();
    if (!lastUserMessage) return;

    setIsLoading(true);
    try {
      const response = await chatAPI.generateSlides(lastUserMessage.content, themeKey);
      setCurrentSlides(response.html);
      setSelectedTheme(themeKey);
      toast.success(`Slides regenerated with ${themes[themeKey]?.name} theme!`);
    } catch (error) {
      console.error('Failed to regenerate slides:', error);
      toast.error('Failed to regenerate slides.');
    } finally {
      setIsLoading(false);
    }
  };

  const downloadSlides = () => {
    if (!currentSlides || typeof window === 'undefined') return;

    const blob = new Blob([currentSlides], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'slides.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success('Slides downloaded!');
  };

  return (
    <div className="h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 overflow-hidden">
      <div className="container mx-auto px-4 py-4 h-full flex flex-col">
        {/* Header */}
        <div className="text-center mb-4">
          <h1 className="text-2xl font-bold text-white mb-1 flex items-center justify-center gap-2">
            <FileText className="text-blue-400" size={24} />
            Markdown-to-Slides Agent
          </h1>
          <p className="text-sm text-gray-300 max-w-xl mx-auto">
            Transform your markdown content into beautiful slide presentations.
          </p>
          {apiStatus && (
            <div className="mt-2 inline-flex items-center gap-2 px-2 py-1 rounded-full text-xs bg-gray-700 text-gray-200 border border-gray-600">
              <div
                className={`w-1.5 h-1.5 rounded-full ${
                  apiStatus.openai_enabled ? 'bg-green-400' : 'bg-yellow-400'
                }`}
              ></div>
              {apiStatus.mode}
            </div>
          )}
        </div>

        <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-4 min-h-0 max-h-full overflow-hidden">
          {/* Chat Interface */}
          <div className="bg-gray-800 rounded-lg shadow-lg border border-gray-700 flex flex-col min-h-0 max-h-full overflow-hidden">
            <div className="border-b border-gray-700 p-3 flex-shrink-0">
              <h2 className="text-base font-semibold text-white flex items-center gap-2">
                <Sparkles className="text-purple-400" size={18} />
                Chat & Generate
              </h2>
            </div>

            <div className="flex-1 min-h-0 max-h-full overflow-hidden">
              <ChatInterface
                messages={messages}
                isLoading={isLoading}
                messagesEndRef={messagesEndRef}
              />
            </div>

            {/* Input Area */}
            <div className="border-t border-gray-700 p-3 flex-shrink-0">
              <div className="flex gap-2 mb-2">
                <button
                  onClick={loadDemoContent}
                  disabled={isLoading}
                  className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white px-3 py-1.5 rounded text-sm transition-colors flex items-center gap-1"
                >
                  <Sparkles size={14} />
                  Try Demo
                </button>
              </div>
              <div className="flex gap-2">
                <textarea
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Type your markdown content here..."
                  className="flex-1 text-white bg-gray-700 resize-none border border-gray-600 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent text-sm placeholder-gray-400"
                  rows={4}
                  disabled={isLoading}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={isLoading || !inputMessage.trim()}
                  className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white px-4 py-2 rounded-lg transition-colors flex items-center gap-2 text-sm self-center "
                >
                  <Send size={20} />
                  Send
                </button>
              </div>
            </div>
          </div>

          {/* Preview & Controls */}
          <div className="bg-gray-800 rounded-lg shadow-lg border border-gray-700 flex flex-col min-h-0">
            <div className="border-b border-gray-700 p-3 flex items-center justify-between">
              <h2 className="text-base font-semibold text-white flex items-center gap-2">
                <Palette className="text-green-400" size={18} />
                Preview & Export
              </h2>
              {currentSlides && (
                <button
                  onClick={downloadSlides}
                  className="bg-green-600 hover:bg-green-700 text-white px-2 py-1 rounded-lg transition-colors flex items-center gap-1 text-xs"
                >
                  <Download size={12} />
                  Download HTML
                </button>
              )}
            </div>

            {currentSlides ? (
              <div className="p-3 flex-1 min-h-0 overflow-y-auto">
                <ThemeSelector
                  themes={themes}
                  selectedTheme={selectedTheme}
                  onThemeChange={regenerateWithTheme}
                  isLoading={isLoading}
                />

                <SlidePreview
                  slidesHtml={currentSlides}
                  showPreview={showPreview}
                  onTogglePreview={() => setShowPreview(!showPreview)}
                />
              </div>
            ) : (
              <div className="p-8 text-center text-gray-400">
                <FileText size={48} className="mx-auto mb-4 text-gray-500" />
                <p>No slides generated yet.</p>
                <p className="text-sm mt-2">
                  Send markdown content to create your first slide deck!
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

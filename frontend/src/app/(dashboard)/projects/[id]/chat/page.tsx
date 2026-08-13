"use client";

import { useState, useEffect, useRef, use } from "react";
import { Send, Bot, User as UserIcon, Loader2 } from "lucide-react";
import api from "@/lib/api";

export default function ChatPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const projectId = resolvedParams.id;
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Keep one session per project so server-persisted history survives refreshes.
    const storageKey = `novax-chat-session:${projectId}`;
    const existingSession = localStorage.getItem(storageKey);
    const nextSession = existingSession ?? crypto.randomUUID();
    if (!existingSession) localStorage.setItem(storageKey, nextSession);
    setSessionId(nextSession);

    const loadHistory = async () => {
      try {
        const response = await api.get(`/projects/${projectId}/chat/${nextSession}`);
        setMessages(Array.isArray(response.data) ? response.data : []);
      } catch (err: any) {
        // A missing project is handled by the page's normal request path; an empty
        // session is a valid first-use state and should not render a raw error.
        if (err?.response?.status !== 404) console.error("Unable to load chat history", err);
      }
    };
    loadHistory();
  }, [projectId]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading || !sessionId) return;

    const userMessage = input.trim();
    setInput("");
    
    // Add locally immediately
    setMessages(prev => [...prev, { role: "user", content: userMessage }]);
    setLoading(true);

    try {
      const res = await api.post(`/projects/${projectId}/chat`, {
        message: userMessage,
        session_id: sessionId
      });
      
      setMessages(prev => [...prev, { role: "assistant", content: res.data.response }]);
    } catch (err: any) {
      if (err?.response?.status !== 404) console.error(err);
      setMessages(prev => [...prev, { role: "assistant", content: "Sorry, I encountered an error. Please try again." }]);

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-12rem)] bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
      
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 flex justify-between items-center">
        <div>
          <h2 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Bot className="w-5 h-5 text-blue-500" />
            AI Co-Founder
          </h2>
          <p className="text-xs text-gray-500 dark:text-gray-400">Contextually aware of your entire startup profile</p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center text-gray-500 dark:text-gray-400 space-y-4">
            <Bot className="w-12 h-12 text-gray-300 dark:text-gray-600" />
            <div>
              <p className="font-medium text-gray-700 dark:text-gray-300">Welcome to your AI Co-Founder!</p>
              <p className="text-sm mt-1 max-w-md">I have full context on your problem space, innovation DNA, business model, market intelligence, and financials. Ask me anything.</p>
            </div>
            <div className="flex flex-wrap justify-center gap-2 mt-4">
              <button onClick={() => setInput("Identify the top 3 biggest risks in my business model.")} className="text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 px-3 py-1.5 rounded-full transition-colors">Top 3 Risks?</button>
              <button onClick={() => setInput("How can I improve my pricing strategy?")} className="text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 px-3 py-1.5 rounded-full transition-colors">Improve Pricing?</button>
              <button onClick={() => setInput("Help me write an email to a Seed investor.")} className="text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 px-3 py-1.5 rounded-full transition-colors">Draft Investor Email</button>
            </div>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex max-w-[80%] gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${msg.role === 'user' ? 'bg-blue-600' : 'bg-gray-900 dark:bg-gray-700'}`}>
                {msg.role === 'user' ? <UserIcon className="w-4 h-4 text-white" /> : <Bot className="w-4 h-4 text-white" />}
              </div>
              <div className={`p-4 rounded-2xl ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-100 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100'}`}>
                <p className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</p>
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
             <div className="flex max-w-[80%] gap-3 flex-row">
               <div className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 bg-gray-900 dark:bg-gray-700">
                  <Bot className="w-4 h-4 text-white" />
               </div>
               <div className="p-4 rounded-2xl bg-gray-100 dark:bg-gray-700/50 flex items-center gap-2">
                 <Loader2 className="w-4 h-4 text-gray-500 animate-spin" />
                 <span className="text-sm text-gray-500">Thinking...</span>
               </div>
             </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
        <form onSubmit={handleSend} className="relative flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading || !sessionId}
            placeholder="Ask your AI Co-Founder..."
            className="w-full pl-4 pr-12 py-3 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-white"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading || !sessionId}
            className="absolute right-2 p-2 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg disabled:opacity-50 transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
        <p className="text-center text-xs text-gray-400 mt-2">AI can make mistakes. Consider verifying important financial or legal advice.</p>
      </div>

    </div>
  );
}

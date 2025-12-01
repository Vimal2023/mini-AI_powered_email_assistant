"use client";

import { useEffect, useState } from "react";
import { useAuth } from "../../hooks/useAuth";
import api from "../api/axios";
import { ChatMessage } from "../../components/ChatMessage";
import { ChatInput } from "../../components/ChatInput";
import { EmailPreviewCard } from "../../components/EmailPreviewCard";

type EmailItem = {
  id: string;
  index: number;
  from: string;
  subject: string;
  summary: string;
};

type ChatItem =
  | { from: "user" | "bot"; text: string }
  | { from: "bot"; emails: EmailItem[] };

export default function DashboardPage() {
  const { user, loading } = useAuth(true);
  const [chat, setChat] = useState<ChatItem[]>([]);

  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    if (!loading && user) {
      setChat([
        {
          from: "bot",
          text: `Hi ${
            user.name || user.email
          }! I can read your last 5 emails, summarize them, and help you reply. Try "read my emails".`,
        },
      ]);
    }
  }, [loading, user]);

  const sendMessage = async (message: string) => {
    setChat((prev) => [...prev, { from: "user", text: message }]);
    setProcessing(true);

    try {
      const res = await api.post("/chat/message", { message });
      const data = res.data;

      if (data.type === "READ" && Array.isArray(data.emails)) {
        setChat((prev) => [
          ...prev,
          { from: "bot", text: "📨 Here are your latest emails:" },
          { from: "bot", emails: data.emails },
        ]);
      } else if (data.message) {
        setChat((prev) => [...prev, { from: "bot", text: data.message }]);
      }
    } catch {
      setChat((prev) => [
        ...prev,
        { from: "bot", text: "⚠ Something went wrong. Try again." },
      ]);
    } finally {
      setProcessing(false);
    }
  };

  if (loading) return <div className="p-6 text-gray-600">Loading...</div>;
  if (!user) return null;

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      {/* HEADER */}
      <header className="border-b bg-white px-6 py-3 flex justify-between items-center shadow-md">
        <h1 className="font-semibold text-lg text-blue-600">
          📧 AI Email Assistant
        </h1>

        <div className="flex items-center gap-4 text-sm">
          <span className="text-gray-600">{user.name || user.email}</span>
          <button
            onClick={() => {
              localStorage.removeItem("token");
              window.location.href = "/login";
            }}
            className="px-3 py-1 bg-red-500 hover:bg-red-600 text-white text-xs rounded-md shadow transition active:scale-95"
          >
            Logout
          </button>
        </div>
      </header>

      {/* CHAT CONTAINER */}
      <main className="flex-1 flex justify-center px-4 py-6">
        <div className="w-full max-w-2xl flex flex-col bg-white shadow-xl rounded-xl p-5 border">
          <div className="flex-1 overflow-y-auto space-y-4 pr-1">
            {chat.map((item, idx) =>
              "emails" in item ? (
                <div key={idx} className="space-y-3">
                  {item.emails.map((email: EmailItem) => (
                    <EmailPreviewCard key={email.id} {...email} />
                  ))}
                </div>
              ) : (
                <ChatMessage key={idx} from={item.from} text={item.text} />
              )
            )}

            {processing && (
              <div className="text-sm text-gray-500 animate-pulse">
                🤖 AI is thinking...
              </div>
            )}
          </div>

          <ChatInput onSend={sendMessage} disabled={processing} />
        </div>
      </main>
    </div>
  );
}

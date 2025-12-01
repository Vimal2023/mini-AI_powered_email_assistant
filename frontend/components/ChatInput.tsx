"use client";
import { useState } from "react";

export function ChatInput({ onSend, disabled }: { onSend: (message: string) => void; disabled: boolean }) {
  const [value, setValue] = useState("");

  const send = () => {
    if (!value.trim()) return;
    onSend(value);
    setValue("");
  };

  return (
    <div className="flex gap-2 mt-4">
      <input
        className="flex-1 border rounded-lg px-3 py-2 text-sm shadow-sm focus:ring-2 focus:ring-blue-500 outline-none transition disabled:bg-gray-200 text-black"
        placeholder="Type a message like — read my emails"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && send()}
        disabled={disabled}
      />
      <button
        onClick={send}
        disabled={disabled}
        className="px-5 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 active:scale-95 text-white text-sm shadow-md transition disabled:bg-gray-400"
      >
        Send
      </button>
    </div>
  );
}

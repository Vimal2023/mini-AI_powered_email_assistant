type Props = {
  from: "user" | "bot";
  text: string;
};

export function ChatMessage({ from, text }: Props) {
  const isUser = from === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} px-1`}>
      <div
        className={`
          max-w-[75%] px-4 py-2 text-sm shadow-md rounded-2xl transition
          ${isUser 
            ? "bg-blue-600 text-white rounded-br-sm hover:bg-blue-700" 
            : "bg-gray-200 text-gray-900 rounded-bl-sm hover:bg-gray-300"
          }
        `}
      >
        {text}
      </div>
    </div>
  );
}

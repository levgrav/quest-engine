import React, { useEffect, useState, useRef } from "react";
import { fetchGameState, sendAction } from "../api/gameApi";
import { useParams } from "react-router-dom";
import "../styles/GamePage.css";  // <-- import the css here

export default function GamePage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const [state, setState] = useState<any>(null);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (sessionId) {
      fetchGameState(sessionId).then(setState).catch(console.error);
    }
  }, [sessionId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [state?.display_messages]);

  const handleSubmit = async () => {
    if (!sessionId || !input) return;
    const updated = await sendAction(sessionId, input);
    setState(updated);
    setInput("");
  };

  return (
    <div className="container">
      <header className="header">
        Game: {state?.name ?? "Loading..."}
      </header>

      <main className="main">
        {state?.display_messages?.map((msg: string, idx: number) => (
          <p key={idx}>{msg}</p>
        ))}
        <div ref={messagesEndRef} />
      </main>

      <footer className="footer">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          placeholder="Enter command..."
          style={{ flex: 1, padding: "0.5rem", borderRadius: "4px", border: "1px solid #ccc" }}
        />
        <button onClick={handleSubmit} style={{ padding: "0.5rem 1rem", borderRadius: "4px", backgroundColor: "#2563eb", color: "white", border: "none" }}>
          Send
        </button>
      </footer>
    </div>
  );
}

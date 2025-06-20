import { useEffect, useState, useRef } from "react";
import { fetchGameState, sendAction } from "../api/gameApi";
import { useParams, useNavigate } from "react-router-dom";
import "../styles/GamePage.css";

export default function GamePage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const [state, setState] = useState<any>(null);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const navigate = useNavigate();

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
      {/* Top Bar */}
      <header className="header">
        <button
          onClick={() => navigate(-1)}
          style={{
            marginRight: "1rem",
            padding: "0.3rem 0.8rem",
            backgroundColor: "#e5e7eb",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          ← Back
        </button>
        <span>Game: {state?.name ?? "Loading..."}</span>
      </header>

      {/* Main Message Area */}
      <main className="main">
        {state?.display_messages?.map((msg: string, idx: number) => (
          <p key={idx}>{msg}</p>
        ))}
        <div ref={messagesEndRef} />
      </main>

      {/* Bottom Bar */}
      <footer className="footer">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          placeholder="Enter command..."
          style={{
            flex: 1,
            padding: "0.5rem",
            borderRadius: "4px",
            border: "1px solid #ccc",
          }}
        />
        <button
          onClick={handleSubmit}
          style={{
            padding: "0.5rem 1rem",
            borderRadius: "4px",
            backgroundColor: "#2563eb",
            color: "white",
            border: "none",
            marginLeft: "0.5rem",
          }}
        >
          Send
        </button>
      </footer>
    </div>
  );
}

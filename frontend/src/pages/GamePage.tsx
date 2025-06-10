import React, { useState } from "react";
import GameConsole from "../components/GameConsole";
import { useNavigate } from "react-router-dom";


export default function GamePage() {
  const navigate = useNavigate();
  const [messages, setMessages] = useState<string[]>([
    "Welcome to the Adventure!",
    "You are in a dark forest.",
    "Type a command to continue...",
  ]);

  const handleCommand = () => {
    setMessages((prev) => [...prev, "You typed a command!"]);
  };

  return (
    <div style={{ padding: "2rem", color: "#fff", backgroundColor: "#222", minHeight: "100vh" }}>
      <h1>Quest for Infinity</h1>
      <GameConsole messages={messages} />
      <button onClick={handleCommand} style={{ marginTop: "1rem" }}>
        Simulate Command
      </button>
      <button onClick={() => navigate(-1)} style={{ marginTop: "1rem" }}>
        Back
      </button>
    </div>
  );
}

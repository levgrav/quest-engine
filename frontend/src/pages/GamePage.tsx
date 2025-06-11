import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchGameState, sendAction } from "../api/gameApi";

export default function GamePage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const [state, setState] = useState<any>(null);
  const [input, setInput] = useState("");

  useEffect(() => {
    if (!sessionId) {
      console.log("No sessionId in URL.");
      return;
    }

    console.log("Loading session", sessionId);

    fetchGameState(sessionId)
      .then((data) => {
        console.log("Game state:", data);
        setState(data);
      })
      .catch((err) => {
        console.error("Error loading game state:", err);
      });
  }, [sessionId]);

  const handleSubmit = async () => {
    if (!sessionId || !input) return;
    const updated = await sendAction(sessionId, input);
    setState(updated);
    setInput("");
  };

  return (
    <div className="p-4 text-white">
      <h2 className="text-xl font-bold mb-2">Game: {sessionId}</h2>
      <pre className="bg-gray-800 p-2 mb-2">{JSON.stringify(state, null, 2)}</pre>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="border p-1 mr-2 text-black"
      />
      <button onClick={handleSubmit} className="bg-blue-500 text-white px-4 py-1 rounded">
        Send
      </button>
    </div>
  );
}

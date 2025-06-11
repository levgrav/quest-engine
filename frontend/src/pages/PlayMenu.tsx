import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchGameInstances, fetchGameTemplates, startGame } from "../api/gameApi";

export default function PlayMenu() {
  const [templates, setTemplates] = useState<string[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchGameTemplates().then(setTemplates).catch(console.error);
  }, []);

  const handleStart = async () => {
    if (!selected) return;
    const { session_id } = await startGame(selected);
    navigate(`/game/${session_id}`);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Choose a Game</h1>
      <ul className="mb-4">
        {templates.map((t) => (
          <li key={t}>
            <button onClick={() => setSelected(t)} className="text-blue-500">
              {t}
            </button>
          </li>
        ))}
      </ul>
      <button onClick={handleStart} disabled={!selected} className="btn">
        Start Game
      </button>
    </div>
  );
}
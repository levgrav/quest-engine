// frontend/src/pages/PlayMenu.tsx
import React, { useEffect, useState } from "react";
import { fetchGameTemplates, startGame, fetchGameInstances } from "../api/gameApi";
import { useNavigate } from "react-router-dom";

export default function PlayMenu() {
  const navigate = useNavigate();
  const [templates, setTemplates] = useState<string[]>([]);
  const [instances, setInstances] = useState<string[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
  const [selectedInstance, setSelectedInstance] = useState<string | null>(null);

  useEffect(() => {
    fetchGameTemplates().then(setTemplates);
    fetchGameInstances().then(setInstances);
  }, []);

  const handleStartNew = async () => {
    if (!selectedTemplate) return;
    const { session_id } = await startGame(selectedTemplate);
    navigate(`/game/${session_id}`);
  };

  const handleLoadInstance = () => {
    if (!selectedInstance) return;
    navigate(`/game/${selectedInstance}`);
  };

  return (
    <div className="p-6 flex flex-col gap-6">
      <h1 className="text-2xl font-bold">Play Menu</h1>

      <div>
        <h2 className="text-lg font-semibold mb-2">Start New Game</h2>
        <ul className="mb-2">
          {templates.map((t) => (
            <li key={t}>
              <button onClick={() => setSelectedTemplate(t)} className="text-blue-500">
                {t}
              </button>
            </li>
          ))}
        </ul>
        <button onClick={handleStartNew} disabled={!selectedTemplate} className="btn">
          Start New
        </button>
      </div>

      <div>
        <h2 className="text-lg font-semibold mb-2">Load Existing Game</h2>
        <ul className="mb-2">
          {instances.map((instance) => (
            <li key={instance}>
              <button onClick={() => setSelectedInstance(instance[0])} className="text-green-600">
                {instance[1]} Last Modified: {instance[2]}
              </button>
            </li>
          ))}
        </ul>
        <button onClick={handleLoadInstance} disabled={!selectedInstance} className="btn">
          Load Game
        </button>
      </div>
    </div>
  );
}

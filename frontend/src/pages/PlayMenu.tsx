// frontend/src/pages/PlayMenu.tsx
import React, { useEffect, useState } from "react";
import { fetchGameTemplates, startGame, fetchGameInstances } from "../api/gameApi";
import { useNavigate } from "react-router-dom";
import "../styles/PlayMenu.css";

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
    <div className="play-container">
      <h1 className="title">Play Menu</h1>

      <div className="section">
        <h2>Start New Game</h2>
        <ul className="template-list">
          {templates.map((t) => (
            <li key={t}>
              <button
                onClick={() => setSelectedTemplate(t)}
                className={`template-button ${selectedTemplate === t ? "selected" : ""}`}
              >
                {t}
              </button>
            </li>
          ))}
        </ul>
        <button
          onClick={handleStartNew}
          disabled={!selectedTemplate}
          className="go-button"
        >
          Start New
        </button>
      </div>

      <div className="section">
        <h2>Load Existing Game</h2>
        <ul className="template-list">
          {instances.map(([id, name, modified]) => (
            <li key={id}>
              <button
                onClick={() => setSelectedInstance(id)}
                className={`template-button ${selectedInstance === id ? "selected" : ""}`}
              >
                {name} — Last Modified: {modified}
              </button>
            </li>
          ))}
        </ul>
        <button
          onClick={handleLoadInstance}
          disabled={!selectedInstance}
          className="go-button"
        >
          Load Game
        </button>
      </div>

      <button onClick={() => navigate(-1)} className="back-button">
        Back
      </button>
    </div>
  );
}
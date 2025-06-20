import React, { useEffect, useState } from "react";
import { fetchGameTemplates } from "../api/gameApi";
import { useNavigate } from "react-router-dom";
import "../styles/CreateMenu.css"; // <-- import your CSS file

export default function CreateMenu() {
  const navigate = useNavigate();
  const [templates, setTemplates] = useState<string[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);

  useEffect(() => {
    fetchGameTemplates().then(setTemplates).catch(console.error);
  }, []);

  const handleCreateNew = () => {
    navigate("/edit/new");
  };

  const handleEditSelected = () => {
    if (!selectedTemplate) return;
    navigate(`/edit/${selectedTemplate}`);
  };

  return (
    <div className="create-container">
      <h1 className="title">Create Menu</h1>

      <div className="section">
        <h2>Edit Existing Project</h2>
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
          onClick={handleEditSelected}
          disabled={!selectedTemplate}
          className="go-button"
        >
          Go
        </button>
      </div>

      <div className="section">
        <h2>Create New Project</h2>
        <button onClick={handleCreateNew} className="new-button">
          Create New Project
        </button>
      </div>

      <button onClick={() => navigate(`/`)} className="back-button">
        Back
      </button>
    </div>
  );
}

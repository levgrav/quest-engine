import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchTemplate, saveTemplate } from "../api/gameApi";

export default function EditorPage() {
  const { templateName } = useParams<{ templateName: string }>();
  const [templateData, setTemplateData] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const [newName, setNewName] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (!templateName) return;
    fetchTemplate(templateName)
      .then((data) => setTemplateData(JSON.stringify(data, null, 2)))
      .catch((err) => {
        console.error("Failed to load template:", err);
        alert("Error loading template.");
        navigate(-1);
      });
  }, [templateName]);

  const handleSave = async () => {
    try {
      const data = JSON.parse(templateData);
      const nameToSave = templateName === "new" ? newName.trim() : templateName;

      if (!nameToSave) {
        setStatus("Please provide a name.");
        return;
      }

      await saveTemplate(nameToSave, data);
      setStatus(`Saved${templateName === "new" ? ` as '${nameToSave}'` : ""}`);
      if (templateName === "new") {
        navigate(`/edit/${nameToSave}`);
      }
    } catch (err) {
      console.error("Save failed:", err);
      setStatus("Save failed. Is your JSON valid?");
    }
  };

  return (
    <div className="p-6 flex flex-col gap-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">
          Editing: {templateName === "new" ? "New Project" : templateName}
        </h1>
        <button onClick={() => navigate(`/create`)} className="btn bg-gray-500 text-white">
          Back
        </button>
      </div>

      {templateName === "new" && (
        <div>
          <label className="block mb-1 font-medium">New Project Name:</label>
          <input
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            className="border p-2 w-full rounded"
            placeholder="Enter project name"
          />
        </div>
      )}

      <textarea
        value={templateData}
        onChange={(e) => setTemplateData(e.target.value)}
        rows={20}
        className="w-full p-2 border rounded font-mono"
      />

      <button onClick={handleSave} className="btn bg-blue-600 text-white hover:bg-blue-700">
        Save
      </button>

      {status && <p className="text-sm text-green-700">{status}</p>}
    </div>
  );
}

import React from "react";
import { useNavigate } from "react-router-dom";


export default function EditorPage() {
  const navigate = useNavigate();

  return (
    <div style={{ color: "white", backgroundColor: "#222", padding: "2rem" }}>
      <h2>Editor Page</h2>
      <p>Here is where the game editing UI will go.</p>
      <button onClick={() => navigate(-1)}>Back</button>
    </div>
  );
}

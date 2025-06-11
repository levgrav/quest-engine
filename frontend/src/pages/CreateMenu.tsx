import React, { useEffect, useState } from "react";
import { fetchGameTemplates } from "../api/gameApi";
import { useNavigate } from "react-router-dom";

export default function CreateMenu() {
  const navigate = useNavigate();
  const [games, setGames] = useState<string[]>([]);

  useEffect(() => {
    fetchGameTemplates().then(setGames).catch(console.error);
  }, []);

  return (
    <div style={styles.container}>
      <h2>Select a Project</h2>
      <ul>
        {games.map((g, i) => (
          <li key={i}>{g}</li>
        ))}
      </ul>
      <button>Create New Project</button>
      <button onClick={() => navigate("/edit")}>Go</button>
      <button onClick={() => navigate(-1)}>Back</button>

    </div>
  );
}

const styles = {
  container: {
    padding: "2rem",
    backgroundColor: "#111",
    color: "#fff",
    minHeight: "100vh",
  },
};

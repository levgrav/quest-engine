import React from "react";
import { useNavigate } from "react-router-dom";

export default function CreateMenu() {
  const navigate = useNavigate();
  const projects = ["Project Alpha", "Lost Forest", "Test World"];

  return (
    <div style={styles.container}>
      <h2>Select a Project</h2>
      <ul>
        {projects.map((p, i) => (
          <li key={i}>{p}</li>
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

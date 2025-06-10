import React from "react";
import { useNavigate } from "react-router-dom";

export default function MainMenu() {
  const navigate = useNavigate();

  return (
    <div style={styles.container}>
      <h1>Quest Engine</h1>
      <button onClick={() => navigate("/create")}>Create</button>
      <button onClick={() => navigate("/play")}>Play</button>
    </div>
  );
}

const styles: { container: React.CSSProperties } = {
  container: {
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
    alignItems: "center",
    justifyContent: "center",
    height: "100vh",
    backgroundColor: "#222",
    color: "#fff",
  },
};

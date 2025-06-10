import React from "react";
import { useNavigate } from "react-router-dom";

export default function PlayMenu() {
  const navigate = useNavigate();
  const games = ["Castle of Night", "Desert Escape", "Mystic River"];

  return (
    <div style={styles.container}>
      <h2>Select a Game</h2>
      <ul>
        {games.map((g, i) => (
          <li key={i}>{g}</li>
        ))}
      </ul>
      <button onClick={() => navigate("/game")}>Go</button>
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

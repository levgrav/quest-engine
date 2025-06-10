import React from "react";

type GameConsoleProps = {
  messages: string[];
};

export default function GameConsole({ messages }: GameConsoleProps) {
  return (
    <div style={styles.console}>
      {messages.map((msg, index) => (
        <div key={index} style={styles.line}>
          {msg}
        </div>
      ))}
    </div>
  );
}

const styles = {
  console: {
    backgroundColor: "#111",
    color: "#0f0",
    padding: "1rem",
    fontFamily: "monospace",
    height: "300px",
    overflowY: "auto",
    border: "1px solid #333",
    borderRadius: "4px",
  },
  line: {
    marginBottom: "0.5rem",
  },
} as const;

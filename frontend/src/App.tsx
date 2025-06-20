// import React from "react";
import { Routes, Route } from "react-router-dom";
import MainMenu from "./pages/MainMenu";
import CreateMenu from "./pages/CreateMenu";
import PlayMenu from "./pages/PlayMenu";
import GamePage from "./pages/GamePage";
import EditorPage from "./pages/EditorPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<MainMenu />} />
      <Route path="/create" element={<CreateMenu />} />
      <Route path="/play" element={<PlayMenu />} />
      <Route path="/game/:sessionId" element={<GamePage />} />
      <Route path="/edit/:templateName" element={<EditorPage />} />
    </Routes>
  );
}

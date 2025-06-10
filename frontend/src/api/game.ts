export async function startGame(playerName: string) {
  const res = await fetch('/game/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ player_name: playerName }),
  });
  return res.json();
}

export async function sendInput(playerName: string, input: string) {
  const res = await fetch('/game/input', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ player_name: playerName, input_text: input }),
  });
  return res.json();
}

export async function saveGame(playerName: string) {
  await fetch('/game/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ player_name: playerName }),
  });
}

export async function loadGame(playerName: string) {
  const res = await fetch('/game/load', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ player_name: playerName }),
  });
  return res.json();
}

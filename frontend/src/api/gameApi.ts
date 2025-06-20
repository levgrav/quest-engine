// frontend/src/api/gameApi.ts
import { get, post } from "./apiClient";

export async function fetchGameTemplates(): Promise<string[]> {
  return get("game/list_templates");
}

export async function fetchGameInstances(): Promise<string[]> {
  return get("game/list_instances");
}

export async function startGame(template: string): Promise<{ session_id: string }> {
  return post("game/new_game", { template });
}

export async function sendAction(sessionId: string, command: string): Promise<any> {
  return post("game/action", { session_id: sessionId, command });
}

export async function fetchGameState(sessionId: string): Promise<any> {
  return get(`game/state/${sessionId}`);
}

export async function fetchTemplate(templateName: string): Promise<any> {
  return get(`game/template/${templateName}`);
}

export async function saveTemplate(templateName: string, data: any): Promise<any> {
  return post(`game/template/${templateName}`, data);
}

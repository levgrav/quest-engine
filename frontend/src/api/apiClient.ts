const BASE_URL = "http://localhost:8000";

export async function get<T>(endpoint: string): Promise<T> {
  const res = await fetch(`${BASE_URL}/${endpoint}`);
  if (!res.ok) throw new Error(`GET ${endpoint} failed`);
  return await res.json();
}

export async function post<T>(endpoint: string, data: any): Promise<T> {
  const res = await fetch(`${BASE_URL}/${endpoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  console.log("hello")
  if (!res.ok) throw new Error(`POST ${endpoint} failed`);
  return await res.json();
}
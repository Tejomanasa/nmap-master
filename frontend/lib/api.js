const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";
const USER_ID = "demo";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    cache: "no-store",
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.detail || "Request failed");
  }
  return payload;
}

export function fetchModules() {
  return request(`/api/modules?user_id=${USER_ID}`);
}

export function acceptEthics() {
  return request(`/api/ethics/accept?user_id=${USER_ID}`, { method: "POST" });
}

export function runScan(command) {
  return request("/api/scan", {
    method: "POST",
    body: JSON.stringify({ command, user_id: USER_ID }),
  });
}

export function completeModule(moduleId, flag) {
  return request("/api/modules/complete", {
    method: "POST",
    body: JSON.stringify({ module_id: moduleId, flag, user_id: USER_ID }),
  });
}

export function generateReport() {
  return request(`/api/report?user_id=${USER_ID}`, { method: "POST" });
}

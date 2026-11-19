
// 📁 Pasta: frontend/src/services/api.js
// Configuração base para chamadas à API Flask

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

/**
 * Faz uma requisição GET à API
 */
export async function apiGet(endpoint) {
  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`[API GET] ${endpoint}:`, error);
    throw error;
  }
}

/**
 * Faz uma requisição POST à API
 */
export async function apiPost(endpoint, body = null) {
  try {
    const options = {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      }
    };

    if (body !== null) {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_URL}${endpoint}`, options);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`[API POST] ${endpoint}:`, error);
    throw error;
  }
}

export default { apiGet, apiPost };


// src/api.js
import axios from "axios";

function getBaseUrlForReal() {
  const raw = (process.env.REACT_APP_API_URL || "http://127.0.0.1:5000").trim();
  // Remove any trailing slashes
  const noTrail = raw.replace(/\/+$/, "");
  // If user already included '/api' at the end, keep it once; otherwise append it
  return noTrail.endsWith("/api") ? noTrail : noTrail + "/api";
}

// For quick debugging, log the resolved base URL at runtime
const BASE_URL = getBaseUrlForReal();
console.info("[API] using baseURL =", BASE_URL);

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 15000,
});

function normalizeError(err) {
  if (!err) return { message: "unknown error" };
  if (err.response) {
    return {
      status: err.response.status,
      data: err.response.data,
      message: err.response.data?.error || err.response.statusText || "server error",
    };
  }
  if (err.request) {
    return { message: "no response from server", details: err.message };
  }
  return { message: err.message || String(err) };
}

export const searchData = async (query, provider, page = 1, per_page = 10) => {
  try {
    const response = await api.post("/search", { query, provider, page, per_page });
    return response.data;
  } catch (error) {
    const e = normalizeError(error);
    // eslint-disable-next-line no-console
    console.error("❌ Error in searchData:", e, error);
    throw e;
  }
};

export const getWeather = async (city) => {
  try {
    const response = await api.get(`/weather?city=${encodeURIComponent(city)}`);
    return response.data;
  } catch (error) {
    const e = normalizeError(error);
    console.error("❌ Error in getWeather:", e, error);
    throw e;
  }
};

export const getNews = async (topic) => {
  try {
    const response = await api.get(`/news?topic=${encodeURIComponent(topic)}`);
    return response.data;
  } catch (error) {
    const e = normalizeError(error);
    console.error("❌ Error in getNews:", e, error);
    throw e;
  }
};

export default api;

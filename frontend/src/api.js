import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000/api", // Flask backend base URL
});

// 🔹 Search API
export const searchData = async (query, provider) => {
  try {
    const response = await api.post("/search", {
      query,
      provider, // matches backend param name
    });
    return response.data;
  } catch (error) {
    console.error("❌ Error in searchData:", error);
    throw error.response ? error.response.data : error;
  }
};

// 🔹 Example for weather (if implemented in backend)
export const getWeather = async (city) => {
  try {
    const response = await api.get(`/weather?city=${city}`);
    return response.data;
  } catch (error) {
    console.error("❌ Error in getWeather:", error);
    throw error.response ? error.response.data : error;
  }
};

// 🔹 Example for news (if implemented in backend)
export const getNews = async (topic) => {
  try {
    const response = await api.get(`/news?topic=${topic}`);
    return response.data;
  } catch (error) {
    console.error("❌ Error in getNews:", error);
    throw error.response ? error.response.data : error;
  }
};

export default api;

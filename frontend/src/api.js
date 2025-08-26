import axios from "axios";

// Use live backend URL from environment variable
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL, // dynamic base URL
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

// 🔹 Example for weather
export const getWeather = async (city) => {
  try {
    const response = await api.get(`/weather?city=${city}`);
    return response.data;
  } catch (error) {
    console.error("❌ Error in getWeather:", error);
    throw error.response ? error.response.data : error;
  }
};

// 🔹 Example for news
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

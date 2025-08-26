import React, { useState } from "react";
import api from "../api";

function SearchForm({ onResultSaved }) {
  const [provider, setProvider] = useState("github");
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    try {
      const res = await api.post("/search", { provider, query });
      setMessage(`✅ Saved ${res.data.summary.items_stored} items from ${provider}`);
      onResultSaved(); // refresh results
      setQuery(""); // clear input
    } catch (err) {
      setMessage("❌ Error: " + (err.response?.data?.error || "Something went wrong"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ marginBottom: "20px", padding: "15px" }}>
      <h2>🔎 Search External API</h2>
      <form onSubmit={handleSubmit}>
        <select value={provider} onChange={(e) => setProvider(e.target.value)}>
          <option value="github">GitHub</option>
          <option value="openweather">OpenWeather</option>
        </select>
        <input
          type="text"
          placeholder="Enter keyword..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          required
          style={{ marginLeft: "10px", marginRight: "10px" }}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default SearchForm;

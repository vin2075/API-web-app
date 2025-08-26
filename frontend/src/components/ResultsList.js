import React, { useEffect, useState } from "react";
import api from "../api";

function ResultsList({ refreshFlag }) {
  const [results, setResults] = useState([]);
  const [currentTimeUTC, setCurrentTimeUTC] = useState("");
  const [currentTimeIST, setCurrentTimeIST] = useState("");

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const res = await api.get("/results");
        setResults(res.data.results);
      } catch (err) {
        console.error("Error fetching results", err);
      }
    };

    fetchResults();

    // Update current time every second
    const interval = setInterval(() => {
      const now = new Date();
      setCurrentTimeUTC(
        now.toLocaleString("en-GB", {
          timeZone: "UTC",
          hour12: true,
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })
      );
      setCurrentTimeIST(
        now.toLocaleString("en-GB", {
          timeZone: "Asia/Kolkata",
          hour12: true,
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })
      );
    }, 1000);

    return () => clearInterval(interval);
  }, [refreshFlag]);

  return (
    <div className="card" style={{ padding: "15px" }}>
      <h2>📊 Dashboard (Stored Results)</h2>
      <p>
        <b>Current Time:</b> UTC: {currentTimeUTC} | IST: {currentTimeIST}
      </p>
      {results.length === 0 ? (
        <p>No results yet.</p>
      ) : (
        <ul style={{ listStyleType: "none", paddingLeft: 0 }}>
          {results.map((r) => (
            <li key={r.id} style={{ marginBottom: "20px" }}>
              <b>{r.provider}</b> → "{r.search_term}" ({r.result.items.length} items)
              <ul style={{ marginTop: "10px" }}>
                {r.provider === "github" &&
                  r.result.items.map((repo) => (
                    <li key={repo.id}>
                      <a href={repo.html_url} target="_blank" rel="noreferrer">
                        {repo.full_name}
                      </a>{" "}
                      - ⭐ {repo.stargazers_count}
                    </li>
                  ))}
                {r.provider === "openweather" &&
                  r.result.items.map((w, idx) => (
                    <li key={idx}>
                      {w.name} - {w.weather[0].description}, Temp: {w.main.temp}°C
                    </li>
                  ))}
              </ul>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default ResultsList;

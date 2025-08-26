import React, { useState } from "react";
import SearchForm from "./SearchForm";
import ResultsList from "./ResultsList";

function Dashboard() {
  const [refreshFlag, setRefreshFlag] = useState(0);

  return (
    <div className="dashboard">
      <SearchForm onResultSaved={() => setRefreshFlag((f) => f + 1)} />
      <ResultsList refreshFlag={refreshFlag} />
    </div>
  );
}

export default Dashboard;

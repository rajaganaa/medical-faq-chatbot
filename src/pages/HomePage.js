import React, { useState, useEffect } from 'react';

const HomePage = () => {
  const [health, setHealth] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/health')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => setHealth(data))
      .catch(error => setError(error.toString()));
  }, []);

  return (
    <div>
      <h1>Home Page</h1>
      <h2>Backend Health Check</h2>
      {error && <p>Error: {error}</p>}
      {health && <pre>{JSON.stringify(health, null, 2)}</pre>}
      {!error && !health && <p>Loading...</p>}
    </div>
  );
};

export default HomePage;

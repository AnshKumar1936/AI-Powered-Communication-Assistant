import React, { useEffect, useState } from 'react';
import Dashboard from './components/Dashboard';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/process_emails')
      .then(res => res.json())
      .then(setData);
  }, []);

  return (
    <div>
      {/* <h1>AI-Powered Communication Assistant</h1> */}
      {data ? <Dashboard data={data} /> : <p>Loading...</p>}
    </div>
  );
}

export default App;
import React, { useState } from 'react';
import EmailCard from './EmailCard';
import '../styles/Dashboard.css';

function Dashboard({ data }) {
  const { urgent_emails, non_urgent_emails, stats } = data;
  const [view, setView] = useState('urgent');

  return (
    <div className="dashboard-dark">
      <header className="dashboard-header">
        <h1>AI-Powered Communication Assistant</h1>
      </header>
      <section className="dashboard-analytics">
        <h2>Analytics</h2>
        <div className="stats-cards">
          <div className="card">Total Emails: {stats.total_emails}</div>
          <div className="card">Last 24h: {stats.last_24h}</div>
          <div className="card">Urgent: {stats.urgent}</div>
          <div className="card">Not Urgent: {stats.not_urgent}</div>
          <div className="card">Sentiment: Positive {stats.sentiment.positive}, Negative {stats.sentiment.negative}, Neutral {stats.sentiment.neutral}</div>
        </div>
        <div className="toggle-buttons">
          <button
            className={view === 'urgent' ? 'active' : ''}
            onClick={() => setView('urgent')}
          >
            Show Urgent Emails
          </button>
          <button
            className={view === 'not_urgent' ? 'active' : ''}
            onClick={() => setView('not_urgent')}
          >
            Show Not Urgent Emails
          </button>
        </div>
      </section>
      <section className="centered-emails">
        {view === 'urgent' ? (
          <>
            <h2>Urgent Emails</h2>
            {urgent_emails.length === 0 ? <p>No urgent emails.</p> : urgent_emails.map((email, idx) => <EmailCard key={idx} email={email} />)}
          </>
        ) : (
          <>
            <h2>Not Urgent Emails</h2>
            {non_urgent_emails.length === 0 ? <p>No not urgent emails.</p> : non_urgent_emails.map((email, idx) => <EmailCard key={idx} email={email} />)}
          </>
        )}
      </section>
    </div>
  );
}

export default Dashboard;
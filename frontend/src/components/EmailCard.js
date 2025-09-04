import React from 'react';

function EmailCard({ email }) {
  return (
    <div className={`email-card ${email.priority === 'Urgent' ? 'urgent' : 'not-urgent'}`}>
      <h3>{email.subject}</h3>
      <p><strong>From:</strong> {email.sender}</p>
      <p><strong>Date:</strong> {email.sent_date}</p>
      <p><strong>Body:</strong> {email.body}</p>
      <p><strong>Sentiment:</strong> {email.sentiment}</p>
      <p><strong>Priority:</strong> {email.priority}</p>
      <p><strong>Extracted Info:</strong> {JSON.stringify(email.info)}</p>
      <div>
        <strong>AI Response:</strong>
        <textarea defaultValue={email.response} rows={4} />
      </div>
    </div>
  );
}

export default EmailCard;
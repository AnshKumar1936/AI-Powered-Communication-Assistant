from flask import Flask, request, jsonify
import pandas as pd
import re
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

app = Flask(__name__)
from flask_cors import CORS
CORS(app)
load_dotenv()

@app.route('/')
def home():
    return "AI-Powered Communication Assistant is running. Use /process_emails to get data."

# --- CONFIG ---
CSV_PATH = "c:\\Users\\kingr\\OneDrive\\Pictures\\Desktop\\Linkenite Project\\68b1acd44f393_Sample_Support_Emails_Dataset.csv"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- FILTERING ---
FILTER_KEYWORDS = ["support", "query", "request", "help"]

# --- PRIORITY ---
URGENT_KEYWORDS = ["immediately", "critical", "urgent", "cannot access", "down", "blocked"]

# --- SENTIMENT (simple heuristic for hackathon) ---
def get_sentiment(text):
    negative_words = ["unable", "error", "problem", "issue", "blocked", "down", "frustrated", "critical"]
    positive_words = ["thank", "appreciate", "great", "resolved", "happy"]
    text_lower = text.lower()
    if any(word in text_lower for word in negative_words):
        return "Negative"
    if any(word in text_lower for word in positive_words):
        return "Positive"
    return "Neutral"

def get_priority(subject, body):
    subject_lower = subject.lower()
    body_lower = body.lower()
    if any(word in subject_lower or word in body_lower for word in URGENT_KEYWORDS):
        return "Urgent"
    return "Not urgent"

def extract_info(body):
    phone = re.findall(r'\b\d{10}\b', body)
    alt_email = re.findall(r'[\w\.-]+@[\w\.-]+', body)
    # Requirements: simple extraction (first sentence)
    requirements = body.split('.')[0]
    return {
        "phone": phone,
        "alt_email": alt_email,
        "requirements": requirements
    }

def generate_response(email_row):
    prompt = f"You are a professional support assistant. Reply to the following email in a friendly, empathetic, and context-aware manner. If the customer is frustrated, acknowledge it. Reference any products or issues mentioned.\n\nSender: {email_row['sender']}\nSubject: {email_row['subject']}\nBody: {email_row['body']}\nDate: {email_row['sent_date']}\n"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        # Gemini returns the response in 'candidates' -> 'content' -> 'parts'
        return result['candidates'][0]['content']['parts'][0]['text'] if 'candidates' in result and result['candidates'] else "No response from Gemini."
    except Exception as e:
        print("Gemini API error:", e)
        print("Response text:", getattr(response, 'text', 'No response'))
        return f"Error generating response: {e}"
    

@app.route('/process_emails', methods=['GET'])
def process_emails():
    df = pd.read_csv(CSV_PATH)
    # Filter emails
    filtered = df[df['subject'].str.lower().str.contains('|'.join(FILTER_KEYWORDS))]
    # Process and sort by priority
    urgent_emails = []
    non_urgent_emails = []
    MAX_API_CALLS = 5  # Limit Groq API calls per request
    api_calls = 0
    for _, row in filtered.iterrows():
        info = extract_info(row['body'])
        sentiment = get_sentiment(row['body'])
        priority = get_priority(row['subject'], row['body'])
        if priority == "Urgent":
            if api_calls < MAX_API_CALLS:
                response = generate_response(row)
                api_calls += 1
            else:
                response = "AI response not generated due to rate limit. Please try again later."
            urgent_emails.append({
                "sender": row['sender'],
                "subject": row['subject'],
                "body": row['body'],
                "sent_date": row['sent_date'],
                "info": info,
                "sentiment": sentiment,
                "priority": priority,
                "response": response
            })
        else:
            non_urgent_emails.append({
                "sender": row['sender'],
                "subject": row['subject'],
                "body": row['body'],
                "sent_date": row['sent_date'],
                "info": info,
                "sentiment": sentiment,
                "priority": priority,
                "response": "AI response not generated for non-urgent emails due to quota limits."
            })
    # Analytics
    total = len(filtered)
    last_24h = filtered[filtered['sent_date'] >= (datetime.now() - pd.Timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')]
    stats = {
        "total_emails": total,
        "last_24h": len(last_24h),
        "urgent": len(urgent_emails),
        "not_urgent": len(non_urgent_emails),
        "sentiment": {
            "positive": sum(e['sentiment'] == "Positive" for e in urgent_emails + non_urgent_emails),
            "negative": sum(e['sentiment'] == "Negative" for e in urgent_emails + non_urgent_emails),
            "neutral": sum(e['sentiment'] == "Neutral" for e in urgent_emails + non_urgent_emails)
        }
    }
    return jsonify({
        "urgent_emails": urgent_emails,
        "non_urgent_emails": non_urgent_emails,
        "stats": stats
    })

if __name__ == "__main__":
    app.run(debug=True)
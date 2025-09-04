# AI-Powered Communication Assistant

## Project Summary
This project is an AI-Powered Communication Assistant designed to help modern organizations efficiently manage support-related emails. It automatically retrieves, filters, categorizes, and prioritizes incoming emails, extracts key information, and generates context-aware, professional responses using advanced LLMs (Gemini, Claude, Groq, etc.). The results are displayed on a user-friendly dashboard with analytics and interactive features to improve response quality and customer satisfaction while reducing manual effort.

## Features
- Email retrieval and filtering (from CSV for demo, can be extended to IMAP/Gmail/Outlook)
- Sentiment analysis and priority detection
- Information extraction (contact details, requirements, metadata)
- Context-aware AI-generated responses for urgent emails
- Analytics dashboard with stats and interactive graphs
- Modern React frontend with toggleable views for urgent and non-urgent emails

## Getting Started

### 1. Backend (Python/Flask)

#### Install dependencies
```
pip install flask pandas requests flask-cors
```

#### Start the backend server
```
python app.py
```
The backend will run at `http://localhost:5000`.

### 2. Frontend (React)

#### Go to the frontend directory
```
cd frontend
```

#### Install dependencies
```
npm install
```

#### Start the frontend server
```
npm start
```
The frontend will run at `http://localhost:3000` and connect to the backend for data.

## Usage
- Open the frontend in your browser.
- View analytics and toggle between urgent and non-urgent emails.
- Review and edit AI-generated responses before sending.

## Customization
- To use a different LLM API (Gemini, Claude, Groq, OpenAI), update the `generate_response` function in `app.py` and set your API key.
- To connect to a real email provider, replace the CSV loading logic with IMAP/Gmail/Outlook integration.

## License
This project is for educational and hackathon use. Extend and customize as needed!

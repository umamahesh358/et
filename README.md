# ET News Copilot

AI-native news experience.

## Setup Instructions

1. Create a virtual environment: 
   ```bash
   python -m venv venv
   ```
2. Activate it:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. Install dependencies: 
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and add your Groq API key.

## Checking if Setup is Correct (Run Instructions)

1. **Start the Backend:**
   Open a terminal, make sure your virtual environment is activated, and run:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   *You should see a message saying Uvicorn is running on http://127.0.0.1:8000.*

2. **Start the Frontend:**
   Open a *second* terminal, activate the virtual environment, and run:
   ```bash
   cd frontend
   streamlit run streamlit_app.py
   ```
   *A browser window should open automatically at http://localhost:8501 showing the starter web page.*

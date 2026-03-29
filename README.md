# 📰 ET News Copilot (Hackathon Edition)

An AI-native, multi-agent news platform built to revolutionize information consumption. ET News Copilot acts as your intelligent assistant, capable of instantly summarizing long-form articles, answering your semantic questions, and generating **high-retention vernacular TikTok/Reels-style videos** autonomously.

![ET News Copilot Banner](https://via.placeholder.com/1000x300.png?text=ET+News+Copilot+-+AI+Native+News)

---

## 🌟 Key Features

1. **🧠 Smart AI Briefings:** Powered by Groq/Llama-3, instantly generate detailed structured summaries from massive articles. Filter outputs by personas (e.g., Investor, Student, Executive).
2. **🔗 Semantic "Related" Search:** Automatically searches a ChromaDB vector database to find and recommend highly relevant past articles based on contextual meaning rather than exact keywords.
3. **🗣️ Vernacular Audio Generation:** Leverages Sarvam AI to natively translate and synthesize natural human voiceovers in Indian languages (Hindi, Tamil, Telugu, etc.).
4. **🎬 Auto-Pilot Video Studio:** An autonomous multi-agent factory that storyboards a script, fetches relevant API-driven 4K imagery, records voiceovers, and compiles a ready-to-publish MP4 using `MoviePy` and `Pillow`.

---

## 🛠️ Tech Stack & Architecture

- **Frontend Interface:** Streamlit (Python)
- **Backend API:** FastAPI
- **LLM / Analytics Engine:** Groq (Llama3-70b-8192)
- **Voice / Translation:** Sarvam AI API
- **Visuals / Generation:** Hugging Face Inference API / LoremFlickr (Fallback Protocol)
- **Vector Database:** ChromaDB + SentenceTransformers (`all-MiniLM-L6-v2`)
- **Video Assembly:** MoviePy (FFmpeg wrapper)

*(For a deep diagnostic look at the Multi-Agent relationships & Workflow Diagrams, see [ARCHITECTURE.md](ARCHITECTURE.md))*

---

## 🚀 Local Installation & Setup

### 1. Requirements
* Python 3.9+
* Active API keys for Groq and Sarvam AI.

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/et-news-copilot.git
cd et-news-copilot
```

### 3. Install Dependencies
```bash
# In the root directory, install the required packages
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the `backend/.env.example` to `backend/.env` (or create it root/backend). Place your secure keys in the `.env` file:
```env
# .env
GROQ_API_KEY=your_groq_api_key_here
SARVAM_API_KEY=your_sarvam_api_key_here
HF_TOKEN=your_hugging_face_token_here # Optional (Failsafes to LoremFlickr photos if empty/rate-limited)
```

---

## 🕹️ Running the Application

Because this app utilizes a decoupled architecture, you must run both the FastAPI Backend and the Streamlit Frontend simultaneously.

### Terminal 1: Start the Backend (FastAPI)
```bash
cd backend
python -m uvicorn main:app --reload
```
*The backend will boot up at `http://127.0.0.1:8000`. You can test endpoints via `http://127.0.0.1:8000/docs`.*

### Terminal 2: Start the Frontend (Streamlit)
```bash
cd frontend
streamlit run streamlit_app.py
```
*Your browser will instantly open at `http://localhost:8501`. Paste an article and you're good to go!*

---

## 🛡️ Hackathon Failsafes Built-In

*   **HF Token Bypass:** If Hugging Face heavily throttles standard inference for Visual generation (503s/403s), the API autonomously fails over to a high-quality static photography proxy (`LoremFlickr`) to ensure video demos never crash on stage.
*   **10-Minute Timeout Protection:** The Streamlit frontend uses extended `requests` timeouts to accommodate heavy background CPU compiling via MoviePy.

---

*Built with ❤️ for the Economic Times Hackathon.*

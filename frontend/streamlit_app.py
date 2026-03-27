import streamlit as st
import requests

# This is where our FastAPI backend lives
API_URL = "http://127.0.0.1:8000/api"

# 1. Clean App Title & Setup
st.set_page_config(page_title="ET News Copilot", page_icon="💥", layout="wide", initial_sidebar_state="expanded")

# --- MASTER CSS INJECTION FOR ET INDIA NEWSROOM THEME ---
CUSTOM_CSS = """
<style>
    /* ET Brand Fonts: Classic Serif for Headers + Clean Sans for Body */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit Clutter */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Clean, High-Contrast Premium Newsroom Background */
    .stApp {
        background-color: #F8F9FA; /* Crisp off-white paper feel */
        color: #1A1A1A; 
    }
    
    /* Sidebar - Sharp Dark Contrast with ET Red Accent */
    [data-testid="stSidebar"] {
        background: #111111 !important; /* Deep black newspaper ink */
        color: #FFFFFF !important;
        border-right: 4px solid #E01A22; /* ET Signature Red border */
    }
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    
    /* The ET Copilot Title */
    h1 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 900 !important;
        color: #E01A22 !important; /* ET Signature Red */
        border-bottom: 3px solid #E01A22;
        padding-bottom: 15px;
        margin-bottom: 25px;
        letter-spacing: -0.5px;
        text-transform: uppercase;
    }

    h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #1A1A1A !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    /* Professional Solid Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 4px; /* Sharper edges for print-news feel */
        background-color: #E01A22 !important; /* ET Red */
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.2s ease-in-out !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 14px !important;
        box-shadow: 0 4px 6px rgba(224, 26, 34, 0.2) !important;
    }
    
    .stButton > button:hover {
        background-color: #B71C1C !important; /* Darker red on hover */
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 14px rgba(224, 26, 34, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(1px) !important;
    }

    /* Clean, High-Contrast Input Fields */
    .stTextArea textarea, .stTextInput input {
        border-radius: 4px !important;
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid #CCCCCC !important;
        font-family: 'Inter', sans-serif !important;
        padding: 12px !important;
        font-size: 15px !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #E01A22 !important;
        box-shadow: 0 0 0 2px rgba(224, 26, 34, 0.2) !important;
    }

    /* Newsroom Content Cards (Info, Warning, Success) */
    div.stAlert {
        border-radius: 4px !important;
        border-left: 5px solid #E01A22 !important; /* Signature left border */
        background-color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
        color: #1A1A1A !important;
        padding: 20px !important;
        border-top: 1px solid #EEEEEE;
        border-right: 1px solid #EEEEEE;
        border-bottom: 1px solid #EEEEEE;
    }
    
    hr {
        border-color: #DDDDDD !important;
    }
    
    a {
        color: #E01A22 !important;
        text-decoration: none !important;
        font-weight: 600 !important;
    }
    a:hover {
        text-decoration: underline !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.title("ET News Copilot 💥")
st.markdown("Transform static news into an **interactive, personalized knowledge experience**.")

# 3. Persona Selection (Sidebar)
st.sidebar.header("⚙️ Settings")
st.sidebar.markdown("Who are you reading for?")
persona = st.sidebar.selectbox("Choose your Persona", ["Investor", "Student", "Startup Founder"])

st.sidebar.markdown("---")
st.sidebar.header("📊 Global Database Insights")
st.sidebar.markdown("Find hidden connections across all news.")
btn_insights = st.sidebar.button("Generate Trend Report", use_container_width=True)

# 2. Article Text Input
st.markdown("### 1️⃣ Provide the News")
article_text = st.text_area("Paste Article Text Here", height=200, placeholder="Paste a news article to begin analysis...")

# 4. Action Buttons Layout
st.markdown("### 2️⃣ Analyze & Search")
col1, col2 = st.columns(2)
btn_briefing = col1.button("🧠 Generate Smart Briefing", use_container_width=True, type="primary")
btn_related = col2.button("🔗 Find Related Articles", use_container_width=True)

# 5. Q&A Input Section
st.markdown("### 3️⃣ Ask Questions")
col_q1, col_q2 = st.columns([4, 1])
with col_q1:
    question = st.text_input("💬 Ask a specific question about the news (Search entire database):", label_visibility="collapsed", placeholder="e.g. How much did EV sales grow?")
with col_q2:
    btn_qa = st.button("Ask Copilot", use_container_width=True)

st.divider()

# --- RESULTS DISPLAY ---

# Handle 'Generate Briefing'
if btn_briefing:
    if not article_text:
        st.warning("Please paste an article first!")
    else:
        # 6. Loading state
        with st.spinner(f"Generating briefing optimized for a {persona}..."):
            try:
                res = requests.post(f"{API_URL}/briefing", json={"article_text": article_text, "persona": persona.lower()})
                if res.status_code == 200:
                    data = res.json()
                    st.success("✅ Briefing Generated!")
                    
                    # 5. Display in clean sections/cards
                    col_res1, col_res2 = st.columns(2)
                    with col_res1:
                        st.info(f"**What Happened?**\n\n{data.get('what_happened', 'N/A')}")
                        st.warning(f"**Key Players Involved:**\n\n{data.get('who_involved', 'N/A')}")
                    with col_res2:
                        st.success(f"**Why it matters to a {persona}:**\n\n{data.get('why_it_matters', 'N/A')}")
                        st.error(f"**What to watch next:**\n\n{data.get('what_next', 'N/A')}")

                    # --- PHASE 11: VOICE SUMMARY ---
                    st.divider()
                    st.markdown("### 🎙️ Listen to AI Briefing")
                    
                    audio_col1, audio_col2 = st.columns([1, 2])
                    
                    language_map = {
                        "English": "en-IN",
                        "Hindi": "hi-IN",
                        "Telugu": "te-IN",
                        "Tamil": "ta-IN",
                        "Kannada": "kn-IN"
                    }
                    
                    with audio_col1:
                        selected_lang = st.selectbox("Select Language", list(language_map.keys()), key="voice_lang")
                    
                    with audio_col2:
                        st.write(" ") # Spacer
                        if st.button("🔊 Play Audio Summary", use_container_width=True):
                            # Combine the summary points into a voice-friendly script
                            voice_text = f"Here is your AI News Briefing. {data.get('what_happened', '')} This matters because {data.get('why_it_matters', '')}"
                            
                            with st.spinner(f"Generating {selected_lang} audio..."):
                                try:
                                    tts_res = requests.post(
                                        f"{API_URL}/tts", 
                                        json={"text": voice_text, "language_code": language_map[selected_lang]}
                                    )
                                    if tts_res.status_code == 200:
                                        st.audio(tts_res.content, format="audio/wav")
                                    else:
                                        st.error("Could not generate audio summary.")
                                except Exception as e:
                                    st.error(f"Voice Error: {e}")
                else:
                    st.error(f"Backend Error: {res.text}")
            except Exception as e:
                st.error(f"Could not connect to backend FASTAPI server. Did you start it? Error: {e}")

# Handle 'Related Articles'
if btn_related:
    if not article_text:
        st.warning("Please paste an article first! We need context to find related stories.")
    else:
        with st.spinner("Searching millions of vectors (jk, our 10 mock vectors)..."):
            try:
                # We use the first 250 characters of the article as the search query
                res = requests.post(f"{API_URL}/related", json={"query": article_text[:250], "limit": 4})
                if res.status_code == 200:
                    articles = res.json().get("related_articles", [])
                    st.success(f"✅ Found {len(articles)} related articles!")
                    
                    for idx, art in enumerate(articles):
                        with st.expander(f"Similarity: {art['similarity_score']}  |  {art['title']}"):
                            st.write(f"**Date:** {art['date']} | **Source:** {art['source']}")
                            st.write(f"**Tags:** {', '.join(art['tags'])}")
                else:
                    st.error("Backend Error.")
            except Exception as e:
                st.error(f"Connection Error: {e}")

# Handle 'Q&A'
if btn_qa:
    if not question:
        st.warning("Please type a question first!")
    else:
        with st.spinner("Analyzing top articles and citing sources..."):
            try:
                res = requests.post(f"{API_URL}/qa", json={"question": question})
                if res.status_code == 200:
                    data = res.json()
                    st.success("✅ Question Answered!")
                    
                    # Display the answer clearly
                    st.markdown(f"### Answer:\n> {data.get('answer', '')}")
                    
                    # Display Citations nicely
                    citations = data.get("citations", [])
                    if citations:
                        st.markdown("**📖 Sources used to answer this:**")
                        for c in citations:
                            st.caption(f"🔗 {c}")
                else:
                    st.error("Backend Error.")
            except Exception as e:
                st.error(f"Connection Error: {e}")

# Handle 'Global Insights'
if btn_insights:
    with st.sidebar:
        with st.spinner("Analyzing macro database trends..."):
            try:
                res = requests.get(f"{API_URL}/insights")
                if res.status_code == 200:
                    data = res.json()
                    st.success("✅ Insights Ready!")
                    
                    st.markdown("**🔥 Trending Topics:**")
                    for t in data.get("trending_topics", []):
                        st.markdown(f"- {t}")
                        
                    st.markdown("**💡 Why it matters:**")
                    st.info(data.get("why_it_matters", ""))
                else:
                    st.error("Backend Error.")
            except Exception as e:
                st.error(f"Connection Error: {e}")

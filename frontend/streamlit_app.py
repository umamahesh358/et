import streamlit as st
import requests
from bs4 import BeautifulSoup

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
    }
    
    /* Main Area Text Enforcement (Black) - Highly specific to avoid breaking buttons */
    [data-testid="stAppViewBlockContainer"] > div > div > div > div.stMarkdown p,
    [data-testid="stAppViewBlockContainer"] > div > div > div > div.stMarkdown li,
    .stRadio label,
    .stTextArea label,
    .stTextInput label,
    .stRadio div[data-testid="stMarkdownContainer"] p,
    .stTextArea div[data-testid="stMarkdownContainer"] p,
    .stTextInput div[data-testid="stMarkdownContainer"] p {
        color: #1A1A1A !important;
    }
    
    /* Sidebar - Sharp Dark Contrast with ET Red Accent */
    [data-testid="stSidebar"] {
        background: #111111 !important; /* Deep black newspaper ink */
        border-right: 4px solid #E01A22; /* ET Signature Red border */
    }
    
    /* Sidebar Text Enforcement (White) */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] div.stMarkdown *,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }
    
    /* Dropdowns in Sidebar should still have black text inside the dropdown list, but white text when closed */
    [data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: #1A1A1A !important;
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
        border: none !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 6px rgba(224, 26, 34, 0.2) !important;
    }
    
    .stButton > button * {
        color: #FFFFFF !important; /* Force button text to be white */
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 14px !important;
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
    .stTextArea textarea, .stTextInput input, 
    .stTextArea textarea::placeholder, .stTextInput input::placeholder {
        border-radius: 4px !important;
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        -webkit-text-fill-color: #1A1A1A !important; /* Forces text color across browsers */
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
        padding: 20px !important;
        border-top: 1px solid #EEEEEE;
        border-right: 1px solid #EEEEEE;
        border-bottom: 1px solid #EEEEEE;
    }
    
    /* Force explicitly black text on internal elements of alerts */
    div.stAlert * {
        color: #1A1A1A !important;
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

# 2. Article Input Options
st.markdown("### 1️⃣ Provide the News")
input_method = st.radio("How do you want to provide the news?", ["Paste Text", "Paste Link"], horizontal=True)

article_text = ""
if input_method == "Paste Text":
    article_text = st.text_area("Paste Article Text Here", height=200, placeholder="Paste a news article to begin analysis...")
else:
    article_url = st.text_input("Paste Article Link Here", placeholder="https://example.com/news-article")
    if article_url:
        with st.spinner("Fetching article content from URL..."):
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                r = requests.get(article_url, headers=headers, timeout=10)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    # Extract text from paragraphs
                    paragraphs = soup.find_all('p')
                    article_text = " ".join([p.get_text() for p in paragraphs])
                    st.success("Article content extracted successfully!")
                    with st.expander("Show Extracted Text"):
                        st.write(article_text[:1000] + "...")
                else:
                    st.error(f"Failed to fetch article. Status code: {r.status_code}")
            except Exception as e:
                st.error(f"Error fetching URL: {e}")

# 4. Action Buttons Layout
st.markdown("### 2️⃣ Analyze & Search")
col1, col2 = st.columns(2)
btn_briefing = col1.button("🧠 Generate Smart Briefing", use_container_width=True, type="primary")
btn_related = col2.button("🔗 Find Related Articles", use_container_width=True)

# 5. Q&A Input Section
st.markdown("### 3️⃣ Ask Questions")
col_q1, col_q2 = st.columns([4, 1])
with col_q1:
    question = st.text_input("💬 Ask anything about the article you loaded:", label_visibility="collapsed", placeholder="e.g. What is the main impact of this news?")
with col_q2:
    btn_qa = st.button("Ask Copilot", use_container_width=True)

# Handle 'Q&A' immediately here so the answer doesn't render at the absolute bottom of the page
if btn_qa:
    if not question:
        st.warning("Please type a question first!")
    else:
        with st.spinner("Analyzing top articles and citing sources..."):
            try:
                res = requests.post(f"{API_URL}/qa", json={"question": question, "article_text": article_text})
                if res.status_code == 200:
                    data = res.json()
                    st.success("✅ Question Answered!")
                    
                    # Display the answer clearly with high-contrast bounding box
                    st.markdown("### 🤖 Copilot Answer:")
                    st.info(data.get('answer', ''))
                    
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

st.divider()

# --- RESULTS DISPLAY ---

# Initialize session state for briefing data
if "briefing_data" not in st.session_state:
    st.session_state.briefing_data = None
if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None
if "video_bytes" not in st.session_state:
    st.session_state.video_bytes = None

# Handle 'Generate Briefing'
if btn_briefing:
    if not article_text:
        st.warning("Please paste an article first!")
    else:
        st.session_state.audio_bytes = None  # Reset audio when regenerating
        with st.spinner(f"Generating briefing optimized for a {persona}..."):
            try:
                res = requests.post(f"{API_URL}/briefing", json={"article_text": article_text, "persona": persona.lower()})
                if res.status_code == 200:
                    st.session_state.briefing_data = res.json()
                    st.session_state.briefing_data["persona"] = persona
                else:
                    st.error(f"Backend Error: {res.text}")
            except Exception as e:
                st.error(f"Could not connect to backend FASTAPI server. Did you start it? Error: {e}")

# Display briefing if we have data in session state
if st.session_state.briefing_data:
    data = st.session_state.briefing_data
    persona_label = data.get("persona", "Investor")
    
    st.success("✅ Briefing Generated!")
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.info(f"**What Happened?**\n\n{data.get('what_happened', 'N/A')}")
        st.warning(f"**Key Players Involved:**\n\n{data.get('who_involved', 'N/A')}")
    with col_res2:
        st.success(f"**Why it matters to a {persona_label}:**\n\n{data.get('why_it_matters', 'N/A')}")
        st.error(f"**What to watch next:**\n\n{data.get('what_next', 'N/A')}")

    # --- VOICE SUMMARY ---
    st.divider()
    st.markdown("### 🎙️ Listen to AI Briefing")
    
    language_map = {
        "English": "en-IN",
        "Hindi": "hi-IN",
        "Telugu": "te-IN",
        "Tamil": "ta-IN",
        "Kannada": "kn-IN"
    }
    
    audio_col1, audio_col2 = st.columns([1, 2])
    with audio_col1:
        selected_lang = st.selectbox("Select Language", list(language_map.keys()), key="voice_lang")
    with audio_col2:
        st.write(" ")  # Spacer
        if st.button("🔊 Play Audio Summary", use_container_width=True):
            voice_text = f"Here is your AI News Briefing. {data.get('what_happened', '')} This matters because {data.get('why_it_matters', '')}"
            voice_text = voice_text[:450]
            with st.spinner(f"Generating {selected_lang} audio..."):
                try:
                    tts_res = requests.post(
                        f"{API_URL}/tts",
                        json={"text": voice_text, "language_code": language_map[selected_lang]}
                    )
                    if tts_res.status_code == 200:
                        st.session_state.audio_bytes = tts_res.content
                    else:
                        st.error(f"Could not generate audio. Server responded with: {tts_res.text}")
                except Exception as e:
                    st.error(f"Voice Error: {e}")

    # Show audio player persistently if audio was generated
    if st.session_state.audio_bytes:
        st.audio(st.session_state.audio_bytes, format="audio/wav")

    # --- VIDEO GENERATOR ---
    st.divider()
    
    with st.container():
        st.markdown("## 🎬 ET News Studio (Beta)")
        st.markdown("Convert this article into a high-retention TikTok/Reels explainer video with **AI-generated visuals, pacing, and multi-lingual voiceovers**.")
        
        # Add a nice card effect using a container with a border
        video_panel = st.container()
        
        with video_panel:
            vid_col1, vid_col2 = st.columns([1, 2])
            with vid_col1:
                vid_lang = st.selectbox("🗣️ Select Narration Language", list(language_map.keys()), key="vid_lang", help="The AI will translate the script and speak naturally.")
                
            with vid_col2:
                st.write(" ")
                # Action-oriented premium button text
                if st.button("⚡ Generate AI Shorts Video", use_container_width=True, type="primary"):
                    st.session_state.video_bytes = None
                    
                    # Beautiful Demo Progress Status (shows each step visually)
                    with st.status("🎥 AI Studios is directing your video...", expanded=True) as status:
                        st.write("📝 1. Storyboarding the script...")
                        st.write("🎨 2. Painting visual scenes via Stable Diffusion...")
                        st.write(f"🎤 3. Recording {vid_lang} voiceover via Sarvam...")
                        st.write("🎬 4. Assembling final cuts...")
                        
                        try:
                            # The core logic is exactly the same
                            vid_res = requests.post(
                                f"{API_URL}/video",
                                json={"article_text": article_text, "language_code": language_map[vid_lang]},
                                timeout=600  # Increased to 10 minutes to prevent MoviePy processing drops
                            )
                            if vid_res.status_code == 200:
                                st.session_state.video_bytes = vid_res.content
                                status.update(label="✅ Explainer Video Published!", state="complete", expanded=False)
                                st.balloons() # Nice touch for hackathons
                            else:
                                status.update(label="❌ Generation Failed", state="error", expanded=True)
                                st.error(f"Error Details: {vid_res.text}")
                        except Exception as e:
                            status.update(label="❌ Connection Error", state="error", expanded=True)
                            st.error(f"Error: {e}")
                            
            # Clear UI Display (Empty State vs Final Output)
            st.write("")
            if st.session_state.video_bytes:
                st.success("🎉 Your video is ready to share on social media!")
                st.video(st.session_state.video_bytes, format="video/mp4")
            else:
                st.info("💡 **Ready to go viral?** Select a language and click Generate. The autonomous AI takes roughly 30-45 seconds to craft a 5-scene video from scratch.")

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

import streamlit as st
import random
from datetime import datetime
import json
import os
import time
import requests
from streamlit_lottie import st_lottie

# ---- App Configuration ----
st.set_page_config(
    page_title="Growth Mindset Journey",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Helper Functions ----
def load_lottie_url(url: str):
    """Load Lottie animation from URL"""
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None
    except Exception:
        return None

def get_user_data():
    """Initialize or load user data"""
    if 'user_data' not in st.session_state:
        try:
            if os.path.exists('user_data.json'):
                with open('user_data.json', 'r') as f:
                    st.session_state.user_data = json.load(f)
            else:
                initialize_user_data()
        except Exception:
            initialize_user_data()
    return st.session_state.user_data

def initialize_user_data():
    """Create new user data structure"""
    st.session_state.user_data = {
        'challenges': [],
        'reflections': [],
        'achievements': [],
        'streak': 0,
        'last_visit': None
    }

def save_user_data():
    """Save user data to file"""
    with open('user_data.json', 'w') as f:
        json.dump(st.session_state.user_data, f)

def update_streak():
    """Calculate and update user streak"""
    user_data = get_user_data()
    today = datetime.now().strftime('%Y-%m-%d')
    
    if user_data['last_visit'] != today:
        last_visit = user_data['last_visit']
        if last_visit is None:
            user_data['streak'] = 1
        else:
            days_diff = (datetime.strptime(today, '%Y-%m-%d') - 
                        datetime.strptime(last_visit, '%Y-%m-%d')).days
            user_data['streak'] = 1 if days_diff > 1 else user_data['streak'] + 1
        
        user_data['last_visit'] = today
        save_user_data()

# ---- Load Assets ----
growth_animation = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_rnnlxazi.json")
achievement_animation = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_touohxv0.json")
reflection_animation = load_lottie_url("https://assets1.lottiefiles.com/private_files/lf30_GjhcdO.json")

# ---- Custom CSS ----
st.markdown("""
<style>
    :root {
        --primary: #6C63FF;
        --secondary: #FF6584;
        --accent: #43B97F;
        --background: #f8f9fa;
        --text: #333;
    }
    
    .main { background: var(--background); padding: 2rem; }
    
    .custom-header {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        font-size: 2.5rem;
    }
    
    .card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .card:hover { transform: translateY(-5px); }
    
    .streak-counter {
        background: linear-gradient(135deg, #FF9D6C, #FF6584);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 4px 10px rgba(255,101,132,0.3);
    }
    
    .quote-card {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        padding: 2rem;
        border-radius: 15px;
        position: relative;
        overflow: hidden;
    }
    
    .timeline-item {
        padding: 1rem;
        margin: 1rem 0;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .stProgress > div > div > div { background: var(--primary); }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate { animation: fadeIn 0.8s ease forwards; }
    .delay-1 { animation-delay: 0.2s; }
    .delay-2 { animation-delay: 0.4s; }
    .delay-3 { animation-delay: 0.6s; }
</style>
""", unsafe_allow_html=True)

# ---- Initialize Data ----
get_user_data()
update_streak()

# ---- Sidebar ----
with st.sidebar:
    st_lottie(growth_animation, height=200, key="sidebar_anim")
    st.markdown("<h2 style='text-align: center;'>Your Growth Journey</h2>", unsafe_allow_html=True)
    
    # Streak Counter
    user_data = st.session_state.user_data
    st.markdown(f"""
    <div class="streak-counter animate">
        <div style="font-size: 0.9rem; opacity: 0.9;">Current Streak</div>
        <div style="font-size: 2.5rem; font-weight: 700;">{user_data['streak']}</div>
        <div style="font-size: 0.9rem; opacity: 0.9;">Days</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    page = st.radio(
        "Navigate",
        ["🏠 Home", "📅 My Journey", "📚 Resources", "ℹ️ About"],
        label_visibility="collapsed"
    )
    
    # Quick Stats
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Challenges", len(user_data['challenges']))
    with col2:
        st.metric("Reflections", len(user_data['reflections']))
    with col3:
        st.metric("Achievements", len(user_data['achievements']))

# ---- Page Content ----
if "🏠 Home" in page:
    # Header Section
    with st.container():
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("<h1 class='custom-header animate'>Growth Mindset Journey</h1>", unsafe_allow_html=True)
            st.markdown("""
            <div class="animate delay-1">
                <p style="font-size: 1.1rem;">
                    Embrace challenges, learn from setbacks, and celebrate progress. 
                    Your journey to a growth mindset starts here!
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if growth_animation:
                st_lottie(growth_animation, height=200, key="main_anim")

    # Main Columns
    col1, col2 = st.columns([3, 2])

    with col1:
        # Daily Challenge
        with st.container():
            st.markdown("### 🌱 Daily Challenge")
            with st.form("challenge_form"):
                challenge = st.text_area("What's challenging you today?")
                if st.form_submit_button("Submit Challenge"):
                    if challenge:
                        user_data['challenges'].append({
                            "text": challenge,
                            "date": datetime.now().isoformat()
                        })
                        save_user_data()
                        st.success("Challenge recorded! 💪")
                        st.balloons()

        # Reflection Journal
        with st.container():
            st.markdown("### 📖 Daily Reflection")
            with st.form("reflection_form"):
                prompt = random.choice([
                    "What did you learn today?",
                    "How did you overcome a challenge?",
                    "What are you grateful for?",
                    "What will you improve tomorrow?"
                ])
                reflection = st.text_area(prompt)
                if st.form_submit_button("Save Reflection"):
                    if reflection:
                        user_data['reflections'].append({
                            "text": reflection,
                            "date": datetime.now().isoformat(),
                            "prompt": prompt
                        })
                        save_user_data()
                        st.success("Reflection saved! ✨")

    with col2:
        # Achievements
        with st.container():
            st.markdown("### 🏆 Achievements")
            with st.form("achievement_form"):
                achievement = st.text_input("Celebrate a win!")
                if st.form_submit_button("Add Achievement"):
                    if achievement:
                        user_data['achievements'].append({
                            "text": achievement,
                            "date": datetime.now().isoformat()
                        })
                        save_user_data()
                        st.success("Achievement added! 🎉")
                        st.balloons()

        # Motivation
        with st.container():
            st.markdown("### 💡 Daily Motivation")
            quotes = [
                ("The only limit is your mind.", "Unknown"),
                ("Growth begins at the end of your comfort zone.", "Neale Donald Walsch"),
                ("Success is stumbling from failure to failure with no loss of enthusiasm.", "Winston Churchill")
            ]
            quote, author = random.choice(quotes)
            st.markdown(f"""
            <div class="quote-card animate">
                <div style="font-size: 1.2rem; font-style: italic;">{quote}</div>
                <div style="text-align: right; margin-top: 1rem;">— {author}</div>
            </div>
            """, unsafe_allow_html=True)

elif "📅 My Journey" in page:
    st.markdown("<h1 class='custom-header'>Progress Tracker</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Timeline", "Challenges", "Achievements"])
    
    with tab1:
        entries = []
        entries.extend([(c['date'], c['text'], 'challenge') for c in user_data['challenges']])
        entries.extend([(r['date'], r['text'], 'reflection') for r in user_data['reflections']])
        entries.extend([(a['date'], a['text'], 'achievement') for a in user_data['achievements']])
        entries.sort(reverse=True)
        
        if entries:
            for date, text, type_ in entries[:10]:
                emoji = "🔄" if type_ == "challenge" else "💡" if type_ == "reflection" else "🏆"
                st.markdown(f"""
                <div class="timeline-item animate">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="font-size: 2rem;">{emoji}</div>
                        <div>
                            <div style="font-weight: 500; color: var(--text);">{text}</div>
                            <div style="font-size: 0.8rem; color: #666;">{datetime.fromisoformat(date).strftime('%b %d, %Y %H:%M')}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No entries yet. Start your journey on the Home page!")

    with tab2:
        if user_data['challenges']:
            for challenge in reversed(user_data['challenges']):
                st.markdown(f"""
                <div class="card">
                    <div style="color: var(--primary);">🔄 Challenge</div>
                    <div>{challenge['text']}</div>
                    <div style="font-size: 0.8rem; color: #666;">
                        {datetime.fromisoformat(challenge['date']).strftime('%b %d, %Y')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No challenges recorded yet")

    with tab3:
        if user_data['achievements']:
            cols = st.columns(2)
            for idx, achievement in enumerate(reversed(user_data['achievements'])):
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div class="card">
                        <div style="color: var(--accent);">🏆 Achievement</div>
                        <div>{achievement['text']}</div>
                        <div style="font-size: 0.8rem; color: #666;">
                            {datetime.fromisoformat(achievement['date']).strftime('%b %d, %Y')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No achievements recorded yet")

elif "📚 Resources" in page:
    st.markdown("<h1 class='custom-header'>Learning Resources</h1>", unsafe_allow_html=True)
    
    with st.expander("📚 Recommended Books"):
        books = [
            ("Mindset: The New Psychology of Success", "Carol Dweck"),
            ("Grit: The Power of Passion and Perseverance", "Angela Duckworth"),
            ("Atomic Habits", "James Clear")
        ]
        for title, author in books:
            st.markdown(f"**{title}** by *{author}*")
    
    with st.expander("🎥 Video Resources"):
        st.video("https://youtu.be/Yl9TVbAal5s")
        st.video("https://youtu.be/KUWn_TJTrnU")
    
    with st.expander("🧠 Interactive Exercises"):
        st.write("**Mindset Assessment**")
        score = st.slider("Rate your current mindset (1 = fixed, 5 = growth)", 1, 5)
        st.write(f"Your growth mindset score: {score}/5")

elif "ℹ️ About" in page:
    st.markdown("<h1 class='custom-header'>About This App</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <h3>🌟 Our Mission</h3>
        <p>
            This app helps you develop a growth mindset through daily practice,
            reflection, and celebration of progress. Built with ❤️ using Streamlit.
        </p>
        <h3>📖 What is Growth Mindset?</h3>
        <p>
            The concept developed by psychologist Carol Dweck that believes abilities
            can be developed through dedication and hard work.
        </p>
        <h3>📬 Contact</h3>
        <p>Have feedback? Reach out at: example@email.com</p>
    </div>
    """, unsafe_allow_html=True)

# ---- Footer ----
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    Made with ❤️ by Shumaila Aijaz | Growth Mindset March 2025
</div>
""", unsafe_allow_html=True)
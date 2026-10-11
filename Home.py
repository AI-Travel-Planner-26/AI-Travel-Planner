import streamlit as st

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Main background */
    .main { background-color: #f0f4f8; }

    /* Hero banner */
    .hero-banner {
        background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
        padding: 2.5rem 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero-banner h1 { font-size: 2.8rem; margin-bottom: 0.3rem; }
    .hero-banner p  { font-size: 1.15rem; opacity: 0.9; }

    /* Feature cards */
    .feature-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        height: 100%;
        transition: transform 0.2s;
    }
    .feature-card:hover { transform: translateY(-3px); }
    .feature-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
    .feature-title { font-size: 1.1rem; font-weight: 700; color: #1a73e8; margin-bottom: 0.4rem; }
    .feature-desc  { font-size: 0.9rem; color: #555; }

    /* Sidebar */
    .css-1d391kg { background-color: #1a73e8 !important; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.88; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Hero Section ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-banner">
        <h1>✈️ AI Travel Planner</h1>
        <p>Your intelligent companion for planning unforgettable journeys around the world</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Feature Grid ─────────────────────────────────────────────────────────────
st.markdown("## 🌟 What can I help you with today?")

col1, col2, col3, col4 = st.columns(4)

features = [
    ("🗺️", "Plan My Trip", "Generate a complete personalised itinerary with day-by-day activities, hotels and dining."),
    ("📍", "Destination Info", "Explore any destination — top attractions, best seasons, visa tips and cultural notes."),
    ("✏️", "Refine Itinerary", "Already have a plan? Let AI tweak and improve it based on your feedback."),
    ("🎒", "Packing List", "Get a smart, destination-specific packing checklist tailored to your trip."),
]

for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
    with col:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ── Quick-start buttons ───────────────────────────────────────────────────────
st.markdown("### 👇 Get started")
b1, b2, b3, b4 = st.columns(4)
with b1:
    if st.button("🗺️ Plan a Trip", use_container_width=True):
        st.switch_page("pages/1_Plan_Trip.py")
with b2:
    if st.button("📍 Explore Destination", use_container_width=True):
        st.switch_page("pages/2_Destination_Info.py")
with b3:
    if st.button("✏️ Refine Itinerary", use_container_width=True):
        st.switch_page("pages/3_Refine_Itinerary.py")
with b4:
    if st.button("🎒 Packing List", use_container_width=True):
        st.switch_page("pages/4_Packing_List.py")

# ── Stats Row ────────────────────────────────────────────────────────────────
st.markdown("---")
s1, s2, s3, s4 = st.columns(4)
stats = [
    ("🌍", "195+", "Countries Covered"),
    ("🤖", "GPT-4", "AI Powered"),
    ("⚡", "< 30s", "Plan Generated"),
    ("🎯", "100%", "Personalised"),
]
for col, (icon, val, label) in zip([s1, s2, s3, s4], stats):
    with col:
        st.metric(label=f"{icon} {label}", value=val)

# ── Sidebar nav hint ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✈️ AI Travel Planner")
    st.markdown("Use the **sidebar** or the buttons above to navigate between features.")
    st.markdown("---")
    st.info("💡 **Tip:** Start with *Plan a Trip* for a complete AI-generated itinerary!")

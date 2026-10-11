import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Plan My Trip | AI Travel Planner", page_icon="🗺️", layout="wide")

# ── Shared CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .page-header {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        color: white; padding: 1.8rem; border-radius: 10px;
        margin-bottom: 1.5rem; text-align: center;
    }
    .result-box {
        background: white; border-radius: 10px;
        padding: 1.8rem; box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin-top: 1rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        color: white; border: none; border-radius: 8px;
        padding: 0.5rem 1.5rem; font-weight: 600; font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="page-header"><h1>🗺️ Plan My Trip</h1>'
    "<p>Fill in your preferences and let AI craft your perfect itinerary</p></div>",
    unsafe_allow_html=True,
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✈️ AI Travel Planner")
    st.markdown("---")
    st.markdown("**Navigation**")
    if st.button("🏠 Home"):
        st.switch_page("Home.py")
    if st.button("📍 Destination Info"):
        st.switch_page("pages/2_Destination_Info.py")
    if st.button("✏️ Refine Itinerary"):
        st.switch_page("pages/3_Refine_Itinerary.py")
    if st.button("🎒 Packing List"):
        st.switch_page("pages/4_Packing_List.py")

# ── Form ──────────────────────────────────────────────────────────────────────
with st.form("plan_form"):
    col1, col2 = st.columns(2)

    with col1:
        destination = st.text_input(
            "🌍 Destination *",
            placeholder="e.g. Tokyo, Japan",
            help="Enter a city, country or region",
        )
        duration = st.slider("📅 Trip Duration (days)", min_value=1, max_value=30, value=7)
        travelers = st.number_input("👥 Number of Travelers", min_value=1, max_value=20, value=1)

    with col2:
        budget = st.selectbox(
            "💰 Budget Level",
            ["Budget (< $50/day)", "Mid-range ($50–$150/day)", "Luxury (> $150/day)"],
        )
        travel_style = st.selectbox(
            "🎭 Travel Style",
            ["Adventure", "Relaxation", "Cultural", "Business", "Family", "Romantic", "Backpacking"],
        )
        interests = st.multiselect(
            "❤️ Interests",
            [
                "History & Culture",
                "Food & Cuisine",
                "Nature & Wildlife",
                "Art & Museums",
                "Shopping",
                "Nightlife",
                "Sports & Fitness",
                "Photography",
                "Architecture",
                "Beach & Water Sports",
            ],
            default=["History & Culture", "Food & Cuisine"],
        )

    submitted = st.form_submit_button("✨ Generate My Travel Plan", use_container_width=True)

# ── API Call & Result ─────────────────────────────────────────────────────────
if submitted:
    if not destination.strip():
        st.error("⚠️ Please enter a destination.")
    else:
        with st.spinner("🤖 AI is crafting your personalised travel plan... This may take a moment."):
            try:
                payload = {
                    "destination": destination.strip(),
                    "duration": duration,
                    "budget": budget,
                    "travel_style": travel_style,
                    "interests": interests,
                    "travelers": travelers,
                }
                resp = requests.post(f"{BACKEND_URL}/api/planner/generate", json=payload, timeout=90)
                resp.raise_for_status()
                data = resp.json()

                st.success(f"✅ Your {duration}-day plan for **{destination}** is ready!")

                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(f"## 🌏 {destination} — {duration}-Day Itinerary")

                # Trip summary chips
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("📅 Duration", f"{duration} days")
                c2.metric("💰 Budget", budget.split("(")[0].strip())
                c3.metric("🎭 Style", travel_style)
                c4.metric("👥 Travelers", travelers)

                st.markdown("---")
                st.markdown(data["plan"])
                st.markdown("</div>", unsafe_allow_html=True)

                # Download button
                st.download_button(
                    label="📥 Download Itinerary",
                    data=data["plan"],
                    file_name=f"{destination.replace(' ', '_')}_itinerary.txt",
                    mime="text/plain",
                )

                # Save to session state for Refine page
                st.session_state["last_itinerary"] = data["plan"]
                st.session_state["last_destination"] = destination

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")
            except requests.exceptions.HTTPError as e:
                st.error(f"❌ Backend error: {e.response.text}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

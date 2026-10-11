import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Destination Info | AI Travel Planner", page_icon="📍", layout="wide")

st.markdown(
    """
    <style>
    .page-header {
        background: linear-gradient(135deg, #00897b, #004d40);
        color: white; padding: 1.8rem; border-radius: 10px;
        margin-bottom: 1.5rem; text-align: center;
    }
    .result-box {
        background: white; border-radius: 10px;
        padding: 1.8rem; box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin-top: 1rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #00897b, #004d40);
        color: white; border: none; border-radius: 8px;
        padding: 0.5rem 1.5rem; font-weight: 600; font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="page-header"><h1>📍 Destination Explorer</h1>'
    "<p>Discover everything you need to know about your next destination</p></div>",
    unsafe_allow_html=True,
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✈️ AI Travel Planner")
    st.markdown("---")
    st.markdown("**Navigation**")
    if st.button("🏠 Home"):
        st.switch_page("Home.py")
    if st.button("🗺️ Plan a Trip"):
        st.switch_page("pages/1_Plan_Trip.py")
    if st.button("✏️ Refine Itinerary"):
        st.switch_page("pages/3_Refine_Itinerary.py")
    if st.button("🎒 Packing List"):
        st.switch_page("pages/4_Packing_List.py")

# ── Popular destinations quick-select ─────────────────────────────────────────
st.markdown("### 🌟 Popular Destinations")
popular = ["Paris, France", "Tokyo, Japan", "New York, USA", "Bali, Indonesia",
           "Rome, Italy", "Dubai, UAE", "Barcelona, Spain", "Sydney, Australia"]

cols = st.columns(4)
chosen_popular = None
for i, dest in enumerate(popular):
    with cols[i % 4]:
        if st.button(dest, key=f"pop_{i}", use_container_width=True):
            chosen_popular = dest

st.markdown("---")

# ── Input ─────────────────────────────────────────────────────────────────────
default_dest = chosen_popular or st.session_state.get("last_destination", "")
destination = st.text_input(
    "🌍 Enter Destination",
    value=default_dest,
    placeholder="e.g. Istanbul, Turkey",
)

if st.button("🔍 Explore Destination", use_container_width=False):
    if not destination.strip():
        st.error("⚠️ Please enter a destination name.")
    else:
        with st.spinner(f"🔎 Gathering information about **{destination}**..."):
            try:
                resp = requests.post(
                    f"{BACKEND_URL}/api/destination/info",
                    json={"destination": destination.strip()},
                    timeout=60,
                )
                resp.raise_for_status()
                data = resp.json()

                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(f"## 📍 {destination}")
                st.markdown("---")
                st.markdown(data["info"])
                st.markdown("</div>", unsafe_allow_html=True)

                st.download_button(
                    label="📥 Download Destination Guide",
                    data=data["info"],
                    file_name=f"{destination.replace(' ', '_')}_guide.txt",
                    mime="text/plain",
                )

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")
            except requests.exceptions.HTTPError as e:
                st.error(f"❌ Backend error: {e.response.text}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

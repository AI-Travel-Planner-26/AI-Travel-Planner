import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Packing List | AI Travel Planner", page_icon="🎒", layout="wide")

st.markdown(
    """
    <style>
    .page-header {
        background: linear-gradient(135deg, #6a1b9a, #4a148c);
        color: white; padding: 1.8rem; border-radius: 10px;
        margin-bottom: 1.5rem; text-align: center;
    }
    .result-box {
        background: white; border-radius: 10px;
        padding: 1.8rem; box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin-top: 1rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #6a1b9a, #4a148c);
        color: white; border: none; border-radius: 8px;
        padding: 0.5rem 1.5rem; font-weight: 600; font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="page-header"><h1>🎒 Smart Packing List</h1>'
    "<p>Get a personalised packing checklist tailored to your trip</p></div>",
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
    if st.button("📍 Destination Info"):
        st.switch_page("pages/2_Destination_Info.py")
    if st.button("✏️ Refine Itinerary"):
        st.switch_page("pages/3_Refine_Itinerary.py")

# ── Form ──────────────────────────────────────────────────────────────────────
default_dest = st.session_state.get("last_destination", "")

col1, col2 = st.columns(2)
with col1:
    destination = st.text_input(
        "🌍 Destination",
        value=default_dest,
        placeholder="e.g. Bali, Indonesia",
    )
    duration = st.slider("📅 Trip Duration (days)", min_value=1, max_value=30, value=7)

with col2:
    travel_style = st.selectbox(
        "🎭 Travel Style",
        ["Adventure", "Relaxation", "Cultural", "Business", "Family", "Romantic", "Backpacking"],
    )
    season = st.selectbox(
        "🌤️ Travel Season",
        ["Spring", "Summer", "Autumn", "Winter"],
    )

if st.button("🎒 Generate Packing List", use_container_width=False):
    if not destination.strip():
        st.error("⚠️ Please enter a destination.")
    else:
        with st.spinner("🤖 Building your personalised packing list..."):
            try:
                resp = requests.post(
                    f"{BACKEND_URL}/api/itinerary/packing-list",
                    json={
                        "destination": destination.strip(),
                        "duration": duration,
                        "travel_style": travel_style,
                        "season": season,
                    },
                    timeout=60,
                )
                resp.raise_for_status()
                data = resp.json()

                st.success(f"✅ Packing list for **{destination}** is ready!")
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(f"## 🎒 Packing List — {destination}")

                c1, c2, c3 = st.columns(3)
                c1.metric("📅 Duration", f"{duration} days")
                c2.metric("🌤️ Season", season)
                c3.metric("🎭 Style", travel_style)

                st.markdown("---")
                st.markdown(data["packing_list"])
                st.markdown("</div>", unsafe_allow_html=True)

                st.download_button(
                    label="📥 Download Packing List",
                    data=data["packing_list"],
                    file_name=f"{destination.replace(' ', '_')}_packing_list.txt",
                    mime="text/plain",
                )

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")
            except requests.exceptions.HTTPError as e:
                st.error(f"❌ Backend error: {e.response.text}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

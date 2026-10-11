import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Refine Itinerary | AI Travel Planner", page_icon="✏️", layout="wide")

st.markdown(
    """
    <style>
    .page-header {
        background: linear-gradient(135deg, #e65100, #bf360c);
        color: white; padding: 1.8rem; border-radius: 10px;
        margin-bottom: 1.5rem; text-align: center;
    }
    .result-box {
        background: white; border-radius: 10px;
        padding: 1.8rem; box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin-top: 1rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #e65100, #bf360c);
        color: white; border: none; border-radius: 8px;
        padding: 0.5rem 1.5rem; font-weight: 600; font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="page-header"><h1>✏️ Refine Your Itinerary</h1>'
    "<p>Already have a plan? Let AI improve it based on your feedback</p></div>",
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
    if st.button("🎒 Packing List"):
        st.switch_page("pages/4_Packing_List.py")

# ── Auto-load from session state ──────────────────────────────────────────────
saved_itinerary = st.session_state.get("last_itinerary", "")

if saved_itinerary:
    st.info("💾 Your last generated itinerary has been pre-loaded below. Feel free to edit it.")

# ── Inputs ────────────────────────────────────────────────────────────────────
original = st.text_area(
    "📋 Paste Your Existing Itinerary",
    value=saved_itinerary,
    height=280,
    placeholder="Paste or type your current travel itinerary here...",
)

feedback_examples = [
    "Add more food experiences",
    "Replace Day 3 activities with beach activities",
    "Make it more budget-friendly",
    "Add family-friendly activities",
    "Include more outdoor/nature activities",
    "Shorten each day to 2 activities only",
]

st.markdown("**💬 Quick Feedback Suggestions:**")
q_cols = st.columns(3)
selected_feedback = None
for i, example in enumerate(feedback_examples):
    with q_cols[i % 3]:
        if st.button(f"💡 {example}", key=f"fb_{i}", use_container_width=True):
            selected_feedback = example

feedback = st.text_area(
    "✍️ Your Feedback / Change Requests",
    value=selected_feedback or "",
    height=120,
    placeholder="e.g. Add more local food experiences, replace Day 3 with beach activities...",
)

if st.button("🔄 Refine Itinerary", use_container_width=False):
    if not original.strip():
        st.error("⚠️ Please provide your existing itinerary.")
    elif not feedback.strip():
        st.error("⚠️ Please provide feedback or change requests.")
    else:
        with st.spinner("🤖 AI is refining your itinerary..."):
            try:
                resp = requests.post(
                    f"{BACKEND_URL}/api/itinerary/refine",
                    json={"original_itinerary": original, "feedback": feedback},
                    timeout=90,
                )
                resp.raise_for_status()
                data = resp.json()

                st.success("✅ Itinerary successfully refined!")
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown("## ✏️ Refined Itinerary")
                st.markdown("---")
                st.markdown(data["refined_itinerary"])
                st.markdown("</div>", unsafe_allow_html=True)

                st.download_button(
                    label="📥 Download Refined Itinerary",
                    data=data["refined_itinerary"],
                    file_name="refined_itinerary.txt",
                    mime="text/plain",
                )

                # Update session state with refined plan
                st.session_state["last_itinerary"] = data["refined_itinerary"]

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")
            except requests.exceptions.HTTPError as e:
                st.error(f"❌ Backend error: {e.response.text}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

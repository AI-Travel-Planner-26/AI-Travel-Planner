# ✈️ AI Travel Planner

An intelligent travel planning application powered by **OpenAI GPT**, built with a **FastAPI** backend and **Streamlit** frontend — 100% Python.

---

## 🌟 Features

| Feature | Description |
|---|---|
| 🗺️ **Plan My Trip** | Generate a complete, personalised day-by-day itinerary |
| 📍 **Destination Explorer** | Get comprehensive info about any destination in the world |
| ✏️ **Refine Itinerary** | Improve an existing plan based on your feedback |
| 🎒 **Smart Packing List** | Get a customised packing checklist for your trip |

---

## 🏗️ Project Structure

```
ai-travel-planner/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── ai_service.py        # OpenAI GPT integration
│   ├── models.py            # Pydantic request/response models
│   └── routers/
│       ├── planner.py       # POST /api/planner/generate
│       ├── destination.py   # POST /api/destination/info
│       └── itinerary.py     # POST /api/itinerary/refine & /packing-list
├── frontend/
│   ├── Home.py              # Streamlit home page
│   └── pages/
│       ├── 1_Plan_Trip.py
│       ├── 2_Destination_Info.py
│       ├── 3_Refine_Itinerary.py
│       └── 4_Packing_List.py
├── run.py                   # One-command startup script
├── requirements.txt
└── .env.example
```

---

## ⚙️ Setup & Installation

### 1. Clone & navigate
```bash
cd ai-travel-planner
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
```
Open `.env` and set your **OpenAI API key**:
```
OPENAI_API_KEY=sk-...your-key-here...
BACKEND_URL=http://localhost:8000
```

---

## 🚀 Running the Application

### Option A — Single command (recommended)
```bash
python run.py
```

### Option B — Run separately

**Terminal 1 – Backend**
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 – Frontend**
```bash
streamlit run frontend/Home.py
```

---

## 🌐 Access

| Service | URL |
|---|---|
| 🎨 Streamlit Frontend | http://localhost:8501 |
| ⚙️ FastAPI Backend | http://localhost:8000 |
| 📚 Swagger API Docs | http://localhost:8000/docs |
| 📖 ReDoc API Docs | http://localhost:8000/redoc |

---

## 🔑 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/planner/generate` | Generate a full travel plan |
| `POST` | `/api/destination/info` | Get destination information |
| `POST` | `/api/itinerary/refine` | Refine an existing itinerary |
| `POST` | `/api/itinerary/packing-list` | Generate a packing list |
| `GET`  | `/health` | Health check |

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, Uvicorn, OpenAI Python SDK, Pydantic
- **Frontend:** Streamlit, Requests, python-dotenv
- **AI:** OpenAI GPT-3.5-turbo / GPT-4

---

## 📝 Notes

- Requires a valid OpenAI API key (GPT-3.5-turbo is used by default; change in `ai_service.py` to use GPT-4).
- All AI responses are streamed via the REST API — allow 15–30 seconds for plan generation.
- Generated plans can be downloaded as `.txt` files directly from the UI.

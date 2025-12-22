"""
FastAPI backend for Synthium Omega Prime
WITH SEMANTIC NLP INTEGRATION
Created by Sina Golchin & Maysam BaygMuhammady
"""
from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sentence_transformers import SentenceTransformer, util
import uvicorn
import numpy as np
from typing import List, Optional, Dict, Any
import asyncio
from datetime import datetime
import json
import sys
import os

# Add parent directory to path to import synthium_core
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from synthium_core.engine import SynthiumEngine
from synthium_core.vectors import SynthiumVector

# ============================================================================
# 1. INITIALIZE SEMANTIC NLP MODEL & ANCHORS
# ============================================================================

# Load a lightweight, powerful model for semantic similarity
# 'all-MiniLM-L6-v2' is fast, accurate, and runs without a GPU.
print("🧠 Loading Semantic NLP Model...")
nlp_model = SentenceTransformer('all-MiniLM-L6-v2')

# Define "Anchor Sentences" – these are the conceptual poles for each dimension.
# The model will compare user input to these to determine their position.
ANCHORS = {
    "v_high": "I am rushing, moving fast, frantic, panicked, urgent.",
    "v_low":  "I am stuck, frozen, slow, sluggish, paralyzed.",
    "R_high": "I feel resistance, friction, pain, trauma, blocked, hated.",
    "R_low":  "I feel easy, smooth, accepting, allowing, open.",
    "r_high": "I feel connected, loved, understood, resonant, in tune.",
    "r_low":  "I feel lonely, isolated, misunderstood, disconnected.",
    "S_high": "I am confused, chaotic, messy, foggy, overwhelmed.",
    "S_low":  "I am clear, organized, structured, clean, ordered."
}

# Pre-compute embeddings for all anchors once (for performance)
print("📐 Computing Anchor Embeddings...")
ANCHOR_EMBEDDINGS = {key: nlp_model.encode(text) for key, text in ANCHORS.items()}
print("✅ Semantic Engine Ready.")


def _description_to_vector(description: str) -> SynthiumVector:
    """
    CORE UPGRADE: Translates natural language to Synthium Vectors using Semantic Triangulation.
    No more keyword matching. This function understands meaning.
    """
    # 1. Encode the user's description into a semantic vector
    user_embedding = nlp_model.encode(description)

    # 2. Calculate similarity scores against all anchor points
    scores = {}
    for key, anchor_embedding in ANCHOR_EMBEDDINGS.items():
        # Cosine similarity: 1 = identical meaning, -1 = opposite meaning
        similarity = util.cos_sim(user_embedding, anchor_embedding)
        scores[key] = float(similarity[0][0])  # Convert tensor to plain float

    # 3. Calculate each dimension by comparing positive and negative anchors
    #    Uses a sigmoid to smooth the result between 0 and 1.
    def calculate_dimension(positive_key, negative_key):
        delta = scores[positive_key] - scores[negative_key]
        # Sigmoid maps delta (-∞ to +∞) to a smooth 0-1 range.
        # The factor of 5 controls the sensitivity of the transition.
        return 1.0 / (1.0 + np.exp(-5 * delta))

    v = calculate_dimension("v_high", "v_low")
    R = calculate_dimension("R_high", "R_low")
    r = calculate_dimension("r_high", "r_low")
    S = calculate_dimension("S_high", "S_low")

    # 4. Capacity (C) is harder to infer from text alone.
    #    We model it as being drained by entropy (S).
    #    High chaos (S) -> Lower capacity (C).
    C = 1.0 - (S * 0.5)  # Basic inverse correlation
    C = max(0.1, min(1.0, C))  # Keep within bounds

    return SynthiumVector(v=v, R=R, r=r, C=C, S=S)


# ============================================================================
# 2. INITIALIZE FASTAPI APP & SYNTHIUM ENGINE
# ============================================================================

app = FastAPI(
    title="Synthium Omega Prime API",
    description="Unified framework for quantifying consciousness and reality - NOW WITH SEMANTIC NLP",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the core Synthium Engine
engine = SynthiumEngine()
print("⚙️ Synthium Core Engine Initialized.")

# Security (placeholder for production)
security = HTTPBearer()

# In-memory session store (replace with database in production)
user_sessions = {}

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()


# ============================================================================
# 3. API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "api": "Synthium Omega Prime",
        "version": "2.1.0",
        "status": "operational",
        "nlp_capability": "semantic_embedding_v1",
        "created_by": "Sina Golchin & Maysam BaygMuhammady",
        "endpoints": {
            "/analyze": "POST - Analyze emotional state (Uses NLP)",
            "/phenomena": "GET - List all phenomena",
            "/phenomena/{id}": "GET - Get specific phenomenon",
            "/transform": "POST - Create transformation plan",
            "/trends": "GET - Analyze user trends",
            "/ws": "WebSocket - Real-time updates"
        }
    }


@app.post("/analyze")
async def analyze_state(
    description: str,
    user_id: str = "anonymous"
):
    """
    Analyze a described emotional/mental state USING SEMANTIC NLP.

    This endpoint translates natural language descriptions into Synthium vectors
    and provides deep insights into consciousness states.
    """
    try:
        print(f"🗣️  User Input: '{description}'")

        # THE CRITICAL UPGRADE: Natural language → Consciousness vector
        vector = _description_to_vector(description)

        print(f"📊 Generated Vector: {vector}")

        # Analyze using the core engine
        analysis = engine.analyze_state(vector)

        # Store in session
        if user_id not in user_sessions:
            user_sessions[user_id] = []

        session_entry = {
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "vector": vector.to_dict(),
            "analysis": analysis
        }
        user_sessions[user_id].append(session_entry)

        # Store in database
        engine.db.add_user_state(user_id, session_entry)

        # Broadcast to websocket clients
        await manager.broadcast({
            "type": "new_analysis",
            "user_id": user_id,
            "data": analysis
        })

        return {
            "user_id": user_id,
            "input": description,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/phenomena")
async def list_phenomena(
    phase: Optional[str] = Query(None, description="Filter by phase"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    limit: Optional[int] = Query(None, description="Limit results")
):
    """
    List all phenomena in the database.

    Can filter by phase (awakening, integration, transcendence, dissolution)
    or by tag (mystical, emotion, mental_health, etc.)
    """
    try:
        if phase:
            phenomena = engine.db.get_phenomena_by_phase(phase)
        elif tag:
            phenomena = engine.db.get_phenomena_by_tag(tag)
        else:
            phenomena = engine.db.get_all_phenomena()

        if limit:
            phenomena = phenomena[:limit]

        return {
            "total": len(phenomena),
            "phenomena": [p.to_dict() for p in phenomena]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch phenomena: {str(e)}")


@app.get("/phenomena/{phenomenon_id}")
async def get_phenomenon(phenomenon_id: int):
    """Get detailed information about a specific phenomenon"""
    try:
        phenomenon = engine.db.get_phenomenon(phenomenon_id)

        if not phenomenon:
            raise HTTPException(status_code=404, detail=f"Phenomenon {phenomenon_id} not found")

        # Get related phenomena
        related = []
        for related_id in phenomenon.related_to:
            related_p = engine.db.get_phenomenon(related_id)
            if related_p:
                related.append({
                    "id": related_p.id,
                    "term": related_p.term,
                    "description": related_p.description
                })

        result = phenomenon.to_dict()
        result["related_phenomena"] = related

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch phenomenon: {str(e)}")


@app.post("/transform")
async def create_transformation(
    current_description: str,
    target_state: str,
    user_id: str = "anonymous"
):
    """
    Create a transformation plan from current state to target state.

    Takes a natural language description of current state and a target state name,
    then generates a step-by-step transformation plan.
    """
    try:
        # Convert current description to vector
        current_vector = _description_to_vector(current_description)

        # Create transformation plan
        plan = engine.create_transformation_plan(current_vector, target_state)

        if "error" in plan:
            raise HTTPException(status_code=400, detail=plan["error"])

        # Store in session
        if user_id not in user_sessions:
            user_sessions[user_id] = []

        user_sessions[user_id].append({
            "timestamp": datetime.now().isoformat(),
            "type": "transformation_plan",
            "current_description": current_description,
            "target_state": target_state,
            "plan": plan
        })

        return {
            "user_id": user_id,
            "current_description": current_description,
            "target_state": target_state,
            "plan": plan,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transformation failed: {str(e)}")


@app.get("/trends")
async def analyze_trends(
    user_id: str = Query(..., description="User ID to analyze"),
    limit: Optional[int] = Query(10, description="Number of recent states to analyze")
):
    """
    Analyze trends in a user's consciousness trajectory over time.

    Provides insights into how their state has evolved.
    """
    try:
        history = engine.db.get_user_history(user_id)

        if not history:
            raise HTTPException(status_code=404, detail=f"No history found for user {user_id}")

        # Get recent trajectory
        trajectory = engine.db.get_user_trajectory(user_id)
        if limit:
            trajectory = trajectory[-limit:]

        if len(trajectory) < 2:
            return {
                "user_id": user_id,
                "message": "Need at least 2 data points for trend analysis",
                "total_states": len(trajectory)
            }

        # Calculate trends
        trends = {
            "v": trajectory[-1].v - trajectory[0].v,
            "R": trajectory[-1].R - trajectory[0].R,
            "r": trajectory[-1].r - trajectory[0].r,
            "C": trajectory[-1].C - trajectory[0].C,
            "S": trajectory[-1].S - trajectory[0].S,
        }

        # Calculate wellbeing trend
        wellbeing_scores = [engine.calculate_wellbeing(v) for v in trajectory]
        wellbeing_trend = wellbeing_scores[-1] - wellbeing_scores[0]

        # Generate insights
        insights = []
        if wellbeing_trend > 0.1:
            insights.append("Overall wellbeing is improving")
        elif wellbeing_trend < -0.1:
            insights.append("Overall wellbeing is declining - may need intervention")

        if trends["S"] > 0.2:
            insights.append("Entropy increasing - life becoming more chaotic")
        elif trends["S"] < -0.2:
            insights.append("Entropy decreasing - finding more clarity and order")

        if trends["r"] > 0.2:
            insights.append("Connection/resonance improving")
        elif trends["r"] < -0.2:
            insights.append("Becoming more disconnected - may need social support")

        return {
            "user_id": user_id,
            "total_states": len(history),
            "analyzed_states": len(trajectory),
            "current_wellbeing": round(wellbeing_scores[-1], 3),
            "wellbeing_trend": round(wellbeing_trend, 3),
            "dimension_trends": {k: round(v, 3) for k, v in trends.items()},
            "insights": insights,
            "trajectory": [v.to_dict() for v in trajectory[-5:]]  # Last 5 states
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trend analysis failed: {str(e)}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time updates.

    Clients can connect here to receive live updates about analyses,
    transformations, and system events.
    """
    await manager.connect(websocket)
    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connection",
            "message": "Connected to Synthium Omega Prime",
            "timestamp": datetime.now().isoformat()
        })

        # Keep connection alive and handle incoming messages
        while True:
            try:
                data = await websocket.receive_json()

                # Handle different message types
                if data.get("type") == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    })
                elif data.get("type") == "analyze":
                    # Real-time analysis
                    description = data.get("description", "")
                    user_id = data.get("user_id", "anonymous")

                    vector = _description_to_vector(description)
                    analysis = engine.analyze_state(vector)

                    await websocket.send_json({
                        "type": "analysis_result",
                        "user_id": user_id,
                        "analysis": analysis,
                        "timestamp": datetime.now().isoformat()
                    })

            except Exception as e:
                print(f"WebSocket error: {e}")
                break

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engine": "operational",
        "nlp_model": "loaded"
    }


# ============================================================================
# 4. CLI FOR RUNNING THE SERVER
# ============================================================================

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    else:
        print("Usage: python app.py run")
        print("Available commands:")
        print("  run - Start the FastAPI server with Semantic NLP")
        print("\nOr use: uvicorn web_backend.app:app --reload")

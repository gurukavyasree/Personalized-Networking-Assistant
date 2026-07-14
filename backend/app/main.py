from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes import router

# Epic 2 Story 8: Core Entry Point Configuration with descriptive Swagger data
app = FastAPI(
    title="AI-Powered Personalized Networking Assistant API",
    description="A modular three-tier API framework hosting theme classification models and conversation generation pipelines.",
    version="1.0.0"
)

# Enable Cross-Origin Resource Sharing (CORS) so the Streamlit UI can talk to the backend smoothly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Centralized API Routing Mount Point containing all core business logic paths
app.include_router(router, prefix="/api")

@app.get("/", tags=["Infrastructure System Tier"])
def root_health_check():
    """
    Production Health-Check Endpoint.
    Allows load balancers, container orchestrators, and external monitors 
    to quickly verify that the API server instance is running and reachable.
    """
    return {
        "status": "healthy",
        "message": "Networking Assistant API is running successfully!"
    }

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.analyze import router as analyze_router

app = FastAPI(title="AI Code Mentor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(analyze_router)


# Root endpoint (optional health check)
@app.get("/")
async def root():
    return {"message": "AI Code Mentor API is running"}
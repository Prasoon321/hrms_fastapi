from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import connect_db, close_db
from app.routes import employee_routes, attendance_routes

# Initialize FastAPI app
app = FastAPI(
    title="HRMS Lite API",
    description="Human Resource Management System - Backend API",
    version="1.0.0"
)

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://hrms-frontend-five-lyart.vercel.app",  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Connect to database on startup"""
    await connect_db()
    print("✓ Application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    await close_db()
    print("✓ Application shutdown complete")


# Health check endpoint
@app.get("/", tags=["health"])
async def root():
    """Health check endpoint"""
    return {
        "message": "HRMS Lite API is running",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Include routes
app.include_router(employee_routes.router)
app.include_router(attendance_routes.router)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle uncaught exceptions"""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

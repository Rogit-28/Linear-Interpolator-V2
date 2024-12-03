"""
Tauri backend integration for the scaling application
This file provides the bridge between the React frontend and the scaling logic
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import sys
import os

# Add the backend directory to the path so we can import scaling_logic
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scaling_logic import scale_coordinates, validate_range_inputs, validate_and_convert_input

app = FastAPI(title="Scaling Range Tauri Backend", version="1.0.0")

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScalingRequest(BaseModel):
    x_input: str
    y_input: str
    z_input: str
    x1: str
    x2: str
    y1: str
    y2: str
    z1: str
    z2: str
    scale_from: str # 'x', 'y', or 'z'
    z_in_hex: bool = False

class ScalingResponse(BaseModel):
    x: str
    y: str
    z: str

class ValidationError(BaseModel):
    error: str

@app.post("/scale", response_model=ScalingResponse, responses={400: {"model": ValidationError}})
async def scale_coordinates_endpoint(request: ScalingRequest):
    """
    Perform scaling calculation based on the specified axis.
    
    Args:
        request: ScalingRequest containing all input values and parameters
        
    Returns:
        ScalingResponse with calculated coordinates
    """
    try:
        # Pass all range values as strings - the new scale_coordinates handles partial data
        result = scale_coordinates(
            request.x_input,
            request.y_input, 
            request.z_input,
            request.x1, request.x2, request.y1, request.y2, request.z1, request.z2,
            scale_from=request.scale_from,
            z_in_hex=request.z_in_hex
        )
        
        return ScalingResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ZeroDivisionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "scaling-range-tauri-backend"}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Scaling Range Tauri Backend API",
        "version": "1.0.0",
        "endpoints": {
            "POST /scale": "Perform scaling calculations",
            "GET /health": "Health check"
        }
    }

def run_server(host: str = "127.0.0.1", port: int = 8001):
    """Run the FastAPI server"""
    uvicorn.run(app, host=host, port=port, log_level="info")

if __name__ == "__main__":
    run_server()

"""
Test script for the scaling API
"""

import asyncio
from scaling_logic import scale_coordinates, validate_range_inputs
from api_server import app, ScalingRequest

def test_scaling_logic_directly():
    """Test the scaling logic directly"""
    print("Testing scaling logic directly...")
    
    # Test X-based scaling
    result = scale_coordinates(
        x_input="5", y_input="", z_input="",
        x1="0", x2="10", y1="0", y2="100", z1="0", z2="50",
        scale_from="x"
    )
    print(f"X-based scaling result: {result}")
    
    # Test Y-based scaling
    result = scale_coordinates(
        x_input="", y_input="50", z_input="",
        x1="0", x2="10", y1="0", y2="100", z1="0", z2="50",
        scale_from="y"
    )
    print(f"Y-based scaling result: {result}")
    
    # Test Z-based scaling
    result = scale_coordinates(
        x_input="", y_input="", z_input="25",
        x1="0", x2="10", y1="0", y2="100", z1="0", z2="50",
        scale_from="z"
    )
    print(f"Z-based scaling result: {result}")
    
    # Test hex conversion
    result = scale_coordinates(
        x_input="5", y_input="", z_input="",
        x1="0", x2="10", y1="0", y2="100", z1="0", z2="10",
        scale_from="x", z_in_hex=True
    )
    print(f"X-based scaling with hex result: {result}")

def test_api_request():
    """Test the API request model"""
    print("\nTesting API request model...")
    
    request = ScalingRequest(
        x_input="5",
        y_input="",
        z_input="",
        x1="0",
        x2="10",
        y1="0",
        y2="100",
        z1="0",
        z2="50",
        scale_from="x",
        z_in_hex=False
    )
    
    print(f"Request model: {request}")
    print(f"Request dict: {request.dict()}")

if __name__ == "__main__":
    test_scaling_logic_directly()
    test_api_request()
    print("\nAll tests completed successfully!")

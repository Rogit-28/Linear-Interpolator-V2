"""
Unit tests for scaling logic
"""

import pytest
from scaling_logic import (
    calculate_scaled_value,
    validate_and_convert_input,
    convert_to_hex_if_needed,
    scale_coordinates,
    validate_range_inputs
)


def test_calculate_scaled_value():
    """Test the core scaling calculation function"""
    # Test basic scaling: 5 in range 0-10 should map to 50 in range 0-100
    result = calculate_scaled_value(5, 0, 10, 0, 100)
    assert result == 50.0
    
    # Test edge cases
    assert calculate_scaled_value(0, 0, 10, 0, 100) == 0.0
    assert calculate_scaled_value(10, 0, 10, 0, 100) == 100.0
    assert calculate_scaled_value(2.5, 0, 10, 0, 100) == 25.0


def test_calculate_scaled_value_division_by_zero():
    """Test division by zero error handling"""
    with pytest.raises(ZeroDivisionError):
        calculate_scaled_value(5, 0, 0, 0, 100)


def test_validate_and_convert_input():
    """Test input validation and conversion"""
    # Test valid decimal inputs
    assert validate_and_convert_input("5.5") == 5.5
    assert validate_and_convert_input("10") == 10.0
    assert validate_and_convert_input("-3.2") == -3.2
    
    # Test empty/whitespace inputs
    assert validate_and_convert_input("") is None
    assert validate_and_convert_input("   ") is None
    assert validate_and_convert_input("-") is None
    
    # Test invalid decimal inputs
    with pytest.raises(ValueError):
        validate_and_convert_input("abc")
    
    # Test hexadecimal conversion
    assert validate_and_convert_input("A", is_hex=True) == 10.0
    assert validate_and_convert_input("0xFF", is_hex=True) == 255.0
    assert validate_and_convert_input("19", is_hex=True) == 25.0
    
    # Test invalid hex input
    with pytest.raises(ValueError):
        validate_and_convert_input("GG", is_hex=True)


def test_convert_to_hex_if_needed():
    """Test hex conversion utility"""
    # Test hex conversion
    assert convert_to_hex_if_needed(255, use_hex=True) == "0xff"
    assert convert_to_hex_if_needed(10, use_hex=True) == "0xa"
    
    # Test no hex conversion
    assert convert_to_hex_if_needed(255, use_hex=False) == 255
    assert convert_to_hex_if_needed(10.5, use_hex=False) == 10.5


def test_scale_coordinates_x_axis():
    """Test scaling based on X axis"""
    result = scale_coordinates(
        x_input="5", y_input="", z_input="",
        x1="0", x2="10", y1="0", y2="100", z1="0", z2="50",
        scale_from="x"
    )
    assert result["x"] == "5"
    assert float(result["y"]) == 50.0  # Should be 5 scaled from 0-10 to 0-100
    assert float(result["z"]) == 25.0  # Should be 5 scaled from 0-10 to 0-50


def test_scale_coordinates_y_axis():
    """Test scaling based on Y axis"""
    result = scale_coordinates(
        x_input="", y_input="50", z_input="",
        x1="0", x2="10", y1="0", y2="100", z1="0", z2="50",
        scale_from="y"
    )
    assert float(result["x"]) == 5.0   # Should be 50 scaled from 0-100 to 0-10
    assert result["y"] == "50"
    assert float(result["z"]) == 25.0  # Should be 50 scaled from 0-100 to 0-50


def test_scale_coordinates_z_axis():
    """Test scaling based on Z axis"""
    result = scale_coordinates(
        x_input="", y_input="", z_input="25",
        x1="0", x2="10", y1="0", y2="100", z1="0", z2="50",
        scale_from="z"
    )
    assert float(result["x"]) == 5.0   # Should be 25 scaled from 0-50 to 0-10
    assert float(result["y"]) == 50.0  # Should be 25 scaled from 0-50 to 0-100
    assert result["z"] == "25"


def test_scale_coordinates_with_hex():
    """Test scaling with hex output for Z values"""
    result = scale_coordinates(
        x_input="5", y_input="", z_input="",
        x1="0", x2="10", y1="0", y2="100", z1="0", z2="10",
        scale_from="x", z_in_hex=True
    )
    assert result["x"] == "5"
    assert float(result["y"]) == 50.0
    assert result["z"] == "0x5"  # Should be hex representation


def test_scale_coordinates_invalid_axis():
    """Test invalid scale_from parameter"""
    with pytest.raises(ValueError):
        scale_coordinates(
            x_input="5", y_input="", z_input="",
            x1="0", x2="10", y1="0", y2="100", z1="0", z2="50",
            scale_from="invalid"
        )


def test_validate_range_inputs():
    """Test range input validation"""
    # Test valid inputs
    result = validate_range_inputs("0", "10", "0", "100", "0", "50")
    assert result == (0.0, 10.0, 0.0, 100.0, 0.0, 50.0)
    
    # Test invalid inputs
    with pytest.raises(ValueError):
        validate_range_inputs("", "10", "0", "100", "0", "50")
    
    with pytest.raises(ValueError):
        validate_range_inputs("0", "10", "invalid", "100", "0", "50")


if __name__ == "__main__":
    pytest.main([__file__])

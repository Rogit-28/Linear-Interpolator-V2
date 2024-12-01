"""
Pure scaling logic without GUI dependencies
Extracted from the original scaling.py application
"""

def calculate_scaled_value(input_value, input_start, input_end, output_start, output_end):
    """
    Calculate scaled value using linear scaling formula.
    
    Args:
        input_value: The value to be scaled
        input_start: Start of input range
        input_end: End of input range  
        output_start: Start of output range
        output_end: End of output range
        
    Returns:
        float: The scaled value
        
    Raises:
        ZeroDivisionError: If input range is zero
        ValueError: If inputs are invalid
    """
    if (input_end - input_start) == 0:
        raise ZeroDivisionError("Input range cannot be zero.")
    
    slope = (output_end - output_start) / (input_end - input_start)
    intercept = output_start - (slope * input_start)
    return slope * input_value + intercept


def validate_and_convert_input(value_str, is_hex=False):
    """
    Validate and convert input string to float.
    
    Args:
        value_str: Input string to validate
        is_hex: Whether the input should be treated as hexadecimal
        
    Returns:
        float: Converted value or None if empty
        
    Raises:
        ValueError: If input is invalid
    """
    if not value_str or value_str.strip() == "":
        return None
    
    if value_str.strip() == "-":
        return None
    
    # Handle hexadecimal conversion for Z values
    if is_hex:
        if value_str.startswith("0x"):
            value_str = value_str[2:]
        
        try:
            decimal_value = int(value_str, 16)
            return float(decimal_value)
        except ValueError:
            raise ValueError("Invalid hexadecimal input!")
    
    # Handle decimal conversion
    try:
        return float(value_str)
    except ValueError:
        raise ValueError("Invalid decimal input!")


def convert_to_hex_if_needed(value, use_hex=False):
    """
    Convert value to hex string if hex format is requested.
    
    Args:
        value: The value to potentially convert
        use_hex: Whether to convert to hex
        
    Returns:
        float or str: Original value or hex string
    """
    if use_hex:
        return hex(int(value))
    return value


def scale_coordinates(x_input, y_input, z_input, x1, x2, y1, y2, z1, z2, scale_from='x', z_in_hex=False):
    """
    Perform scaling based on selected axis.
    
    Args:
        x_input, y_input, z_input: Input coordinates
        x1, x2, y1, y2, z1, z2: Range definitions
        scale_from: 'x', 'y', or 'z' - which coordinate drives scaling
        z_in_hex: Whether Z output should be in hexadecimal
        
    Returns:
        dict: Calculated coordinates
    """
    # Validate and convert range inputs to numbers, but allow some to be empty
    range_values = [x1, x2, y1, y2, z1, z2]
    
    # Try to validate each range pair separately
    x_range_valid = x1 and x2 and x1.strip() and x2.strip() and all(not (v is None or v.strip() == "" or not str(v).strip()) for v in [x1, x2]) and all(not (not str(v).strip() or not str(v).strip().replace('.', '').replace('-', '').isdigit()) for v in [x1, x2])
    y_range_valid = y1 and y2 and y1.strip() and y2.strip() and all(not (v is None or v.strip() == "" or not str(v).strip()) for v in [y1, y2]) and all(not (not str(v).strip() or not str(v).strip().replace('.', '').replace('-', '').isdigit()) for v in [y1, y2])
    z_range_valid = z1 and z2 and z1.strip() and z2.strip() and all(not (v is None or v.strip() == "" or not str(v).strip()) for v in [z1, z2]) and all(not (not str(v).strip() or not str(v).strip().replace('.', '').replace('-', '').isdigit()) for v in [z1, z2])
    
    # Convert to numbers if valid
    try:
        x1_num = float(x1) if x_range_valid and x1 and x1.strip() else None
        x2_num = float(x2) if x_range_valid and x2 and x2.strip() else None
        y1_num = float(y1) if y_range_valid and y1 and y1.strip() else None
        y2_num = float(y2) if y_range_valid and y2 and y2.strip() else None
        z1_num = float(z1) if z_range_valid and z1 and z1.strip() else None
        z2_num = float(z2) if z_range_valid and z2 and z2.strip() else None
    except ValueError:
        raise ValueError("Invalid range values provided")

    if scale_from == 'x':
        input_val = validate_and_convert_input(x_input)
        if input_val is None:
            return {'x': x_input, 'y': '', 'z': ''}
        
        result = {'x': x_input, 'y': '', 'z': ''}
        
        # Calculate Y if X-Y ranges are valid
        if x_range_valid and y_range_valid and x1_num is not None and x2_num is not None and y1_num is not None and y2_num is not None:
            try:
                y = calculate_scaled_value(input_val, x1_num, x2_num, y1_num, y2_num)
                result['y'] = str(y)
            except (ZeroDivisionError, ValueError):
                result['y'] = ''
        
        # Calculate Z if X-Z ranges are valid
        if x_range_valid and z_range_valid and x1_num is not None and x2_num is not None and z1_num is not None and z2_num is not None:
            try:
                z = calculate_scaled_value(input_val, x1_num, x2_num, z1_num, z2_num)
                result['z'] = str(convert_to_hex_if_needed(z, z_in_hex))
            except (ZeroDivisionError, ValueError):
                result['z'] = ''
        
        return result
    
    elif scale_from == 'y':
        input_val = validate_and_convert_input(y_input)
        if input_val is None:
            return {'x': '', 'y': y_input, 'z': ''}
        
        result = {'x': '', 'y': y_input, 'z': ''}
        
        # Calculate X if Y-X ranges are valid
        if y_range_valid and x_range_valid and y1_num is not None and y2_num is not None and x1_num is not None and x2_num is not None:
            try:
                x = calculate_scaled_value(input_val, y1_num, y2_num, x1_num, x2_num)
                result['x'] = str(x)
            except (ZeroDivisionError, ValueError):
                result['x'] = ''
        
        # Calculate Z if Y-Z ranges are valid
        if y_range_valid and z_range_valid and y1_num is not None and y2_num is not None and z1_num is not None and z2_num is not None:
            try:
                z = calculate_scaled_value(input_val, y1_num, y2_num, z1_num, z2_num)
                result['z'] = str(convert_to_hex_if_needed(z, z_in_hex))
            except (ZeroDivisionError, ValueError):
                result['z'] = ''
        
        return result
    
    elif scale_from == 'z':
        input_val = validate_and_convert_input(z_input, is_hex=z_in_hex)
        if input_val is None:
            return {'x': '', 'y': '', 'z': z_input}
        
        result = {'x': '', 'y': '', 'z': z_input}
        
        # Calculate X if Z-X ranges are valid
        if z_range_valid and x_range_valid and z1_num is not None and z2_num is not None and x1_num is not None and x2_num is not None:
            try:
                x = calculate_scaled_value(input_val, z1_num, z2_num, x1_num, x2_num)
                result['x'] = str(x)
            except (ZeroDivisionError, ValueError):
                result['x'] = ''
        
        # Calculate Y if Z-Y ranges are valid
        if z_range_valid and y_range_valid and z1_num is not None and z2_num is not None and y1_num is not None and y2_num is not None:
            try:
                y = calculate_scaled_value(input_val, z1_num, z2_num, y1_num, y2_num)
                result['y'] = str(y)
            except (ZeroDivisionError, ValueError):
                result['y'] = ''
        
        return result
    
    else:
        raise ValueError("scale_from must be 'x', 'y', or 'z'")


def validate_range_inputs(x1, x2, y1, y2, z1, z2):
    """
    Validate that range inputs are valid numbers.
    
    Args:
        x1, x2, y1, y2, z1, z2: Range definition values
        
    Returns:
        tuple: Validated float values
        
    Raises:
        ValueError: If any input is invalid
    """
    inputs = [x1, x2, y1, y2, z1, z2]
    validated = []
    
    for i, inp in enumerate(inputs):
        if inp is None:
            inp = ""
        
        # Convert to string and strip whitespace
        inp_str = str(inp).strip()
        
        if inp_str == "":
            raise ValueError(f"Range value {['x1', 'x2', 'y1', 'y2', 'z1', 'z2'][i]} cannot be empty")
        
        try:
            validated.append(float(inp_str))
        except ValueError:
            raise ValueError(f"Invalid range value: {['x1', 'x2', 'y1', 'y2', 'z1', 'z2'][i]}")
    
    return tuple(validated)

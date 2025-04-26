"""
Validation utilities for data validation
"""
from typing import Any, Optional, List, Dict, Tuple, Union
from datetime import datetime
import re


def validate_date(date_str: Optional[str]) -> Tuple[bool, Optional[str]]:
    """Validate a date string in YYYY-MM-DD format
    
    Args:
        date_str: Date string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if date_str is None:
        return True, None
    
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(date_pattern, date_str):
        return False, "รูปแบบวันที่ไม่ถูกต้อง กรุณาใช้รูปแบบ YYYY-MM-DD"
    
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True, None
    except ValueError:
        return False, "วันที่ไม่ถูกต้อง"


def validate_date_range(start_date: Optional[str], end_date: Optional[str]) -> Tuple[bool, Optional[str]]:
    """Validate a date range
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Validate individual dates
    start_valid, start_error = validate_date(start_date)
    if not start_valid:
        return False, f"วันที่เริ่มต้น: {start_error}"
    
    end_valid, end_error = validate_date(end_date)
    if not end_valid:
        return False, f"วันที่สิ้นสุด: {end_error}"
    
    # If both dates are valid and present, check that end_date >= start_date
    if start_date and end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        if end < start:
            return False, "วันที่สิ้นสุดต้องไม่อยู่ก่อนวันที่เริ่มต้น"
    
    return True, None


def validate_numeric(value: Any, min_value: Optional[float] = None, 
                     max_value: Optional[float] = None, 
                     allow_none: bool = True) -> Tuple[bool, Optional[str]]:
    """Validate a numeric value
    
    Args:
        value: Value to validate
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        allow_none: Whether None is allowed
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if value is None:
        return allow_none, None if allow_none else "ค่าไม่สามารถเป็นค่าว่างได้"
    
    try:
        num_value = float(value)
    except (ValueError, TypeError):
        return False, "ค่าต้องเป็นตัวเลข"
    
    if min_value is not None and num_value < min_value:
        return False, f"ค่าต้องไม่น้อยกว่า {min_value}"
    
    if max_value is not None and num_value > max_value:
        return False, f"ค่าต้องไม่มากกว่า {max_value}"
    
    return True, None


def validate_text(text: Optional[str], min_length: int = 0, 
                  max_length: Optional[int] = None, 
                  allow_none: bool = True) -> Tuple[bool, Optional[str]]:
    """Validate a text value
    
    Args:
        text: Text to validate
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        allow_none: Whether None is allowed
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if text is None or text == "":
        return allow_none, None if allow_none else "ข้อความไม่สามารถเป็นค่าว่างได้"
    
    if min_length > 0 and len(text) < min_length:
        return False, f"ข้อความต้องมีความยาวอย่างน้อย {min_length} ตัวอักษร"
    
    if max_length is not None and len(text) > max_length:
        return False, f"ข้อความต้องมีความยาวไม่เกิน {max_length} ตัวอักษร"
    
    return True, None


def validate_in_list(value: Any, valid_values: List[Any], 
                     allow_none: bool = True) -> Tuple[bool, Optional[str]]:
    """Validate that a value is in a list of valid values
    
    Args:
        value: Value to validate
        valid_values: List of valid values
        allow_none: Whether None is allowed
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if value is None:
        return allow_none, None if allow_none else "ค่าไม่สามารถเป็นค่าว่างได้"
    
    if value not in valid_values:
        valid_str = ", ".join(str(v) for v in valid_values)
        return False, f"ค่าต้องเป็นหนึ่งใน: {valid_str}"
    
    return True, None


def validate_id_exists(id_value: int, get_by_id_func: callable) -> Tuple[bool, Optional[str]]:
    """Validate that an ID exists
    
    Args:
        id_value: ID value to validate
        get_by_id_func: Function to get entity by ID
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if id_value is None:
        return False, "ID ไม่สามารถเป็นค่าว่างได้"
    
    entity = get_by_id_func(id_value)
    if entity is None:
        return False, f"ไม่พบ ID: {id_value}"
    
    return True, None

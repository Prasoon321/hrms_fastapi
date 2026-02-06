import re
from datetime import datetime


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_date_format(date_str: str) -> bool:
    """Validate date format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_attendance_status(status: str) -> bool:
    """Validate attendance status"""
    valid_statuses = ["Present", "Absent", "Half Day", "Leave"]
    return status in valid_statuses


def validate_employee_id_format(employee_id: str) -> bool:
    """Validate employee ID format (EMP followed by digits)"""
    pattern = r'^EMP\d{3,}$'
    return re.match(pattern, employee_id) is not None


def generate_employee_id(employee_count: int) -> str:
    """Generate unique employee ID based on count"""
    return f"EMP{str(employee_count + 1).zfill(3)}"

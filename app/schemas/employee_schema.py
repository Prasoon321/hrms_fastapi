from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class EmployeeCreate(BaseModel):
    """Schema for creating a new employee"""
    full_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    department: str = Field(..., min_length=1, max_length=50)

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Aarav Sharma",
                "email": "aarav@company.com",
                "department": "IT"
            }
        }


class EmployeeResponse(BaseModel):
    """Schema for employee response"""
    employee_id: str
    full_name: str
    email: str
    department: str
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "EMP001",
                "full_name": "Aarav Sharma",
                "email": "aarav@company.com",
                "department": "IT",
                "created_at": "2025-02-06T10:00:00.000000"
            }
        }


class EmployeeList(BaseModel):
    """Schema for employee list response"""
    employees: list[EmployeeResponse]
    total: int

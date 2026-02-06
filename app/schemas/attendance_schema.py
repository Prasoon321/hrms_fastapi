from datetime import datetime
from pydantic import BaseModel, Field


class AttendanceCreate(BaseModel):
    """Schema for creating attendance record"""
    employee_id: str = Field(..., min_length=1)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD format
    status: str = Field(..., min_length=1, max_length=20)

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "EMP001",
                "date": "2025-02-06",
                "status": "Present"
            }
        }


class AttendanceResponse(BaseModel):
    """Schema for attendance response"""
    employee_id: str
    date: str
    status: str
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "EMP001",
                "date": "2025-02-06",
                "status": "Present",
                "created_at": "2025-02-06T10:00:00.000000"
            }
        }


class AttendanceList(BaseModel):
    """Schema for attendance list response"""
    records: list[AttendanceResponse]
    total: int

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str):
            return ObjectId(v)
        raise TypeError(f"ObjectId required, got {type(v)}")


class Attendance(BaseModel):
    """Attendance model for MongoDB"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    employee_id: str  # Reference to employee by ID
    date: str  # Date in YYYY-MM-DD format
    status: str  # Present, Absent, Half Day, Leave
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

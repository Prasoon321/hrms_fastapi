from datetime import datetime
from fastapi import HTTPException, status
from app.database import get_db
from app.schemas.attendance_schema import AttendanceCreate, AttendanceResponse
from app.utils.validators import (
    validate_date_format,
    validate_attendance_status
)


class AttendanceService:
    """Service for attendance operations"""

    @staticmethod
    async def mark_attendance(attendance_data: AttendanceCreate) -> AttendanceResponse:
        """Mark attendance for an employee"""
        db = get_db()
        
        # Validate date format
        if not validate_date_format(attendance_data.date):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use YYYY-MM-DD"
            )
        
        # Validate status
        if not validate_attendance_status(attendance_data.status):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid attendance status. Must be: Present, Absent, Half Day, or Leave"
            )
        
        # Check if employee exists
        employee = await db["employees"].find_one({"employee_id": attendance_data.employee_id})
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee {attendance_data.employee_id} not found"
            )
        
        # Check if attendance already marked for this date
        existing = await db["attendance"].find_one({
            "employee_id": attendance_data.employee_id,
            "date": attendance_data.date
        })
        
        if existing:
            # Update existing record
            await db["attendance"].update_one(
                {"employee_id": attendance_data.employee_id, "date": attendance_data.date},
                {"$set": {"status": attendance_data.status}}
            )
        else:
            # Create new record
            attendance_doc = {
                "employee_id": attendance_data.employee_id,
                "date": attendance_data.date,
                "status": attendance_data.status,
                "created_at": datetime.utcnow()
            }
            await db["attendance"].insert_one(attendance_doc)
        
        return AttendanceResponse(
            employee_id=attendance_data.employee_id,
            date=attendance_data.date,
            status=attendance_data.status,
            created_at=datetime.utcnow()
        )

    @staticmethod
    async def get_all_attendance() -> list[dict]:
        """Get all attendance records with employee details"""
        db = get_db()
        
        # Pipeline to join with employees collection
        pipeline = [
            {
                "$lookup": {
                    "from": "employees",
                    "localField": "employee_id",
                    "foreignField": "employee_id",
                    "as": "employee_info"
                }
            },
            {"$sort": {"date": -1, "created_at": -1}},
            {"$unwind": {"path": "$employee_info", "preserveNullAndEmptyArrays": True}}
        ]
        
        records = await db["attendance"].aggregate(pipeline).to_list(None)
        
        result = []
        for record in records:
            employee_info = record.get("employee_info", {})
            result.append({
                "employee_id": record["employee_id"],
                "employee_name": employee_info.get("full_name", "Unknown"),
                "date": record["date"],
                "status": record["status"],
                "created_at": record.get("created_at")
            })
        
        return result

    @staticmethod
    async def get_attendance_by_employee(employee_id: str) -> list[AttendanceResponse]:
        """Get attendance records for a specific employee"""
        db = get_db()
        
        # Check if employee exists
        employee = await db["employees"].find_one({"employee_id": employee_id})
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee {employee_id} not found"
            )
        
        records = await db["attendance"].find(
            {"employee_id": employee_id}
        ).sort("date", -1).to_list(None)
        
        return [
            AttendanceResponse(
                employee_id=record["employee_id"],
                date=record["date"],
                status=record["status"],
                created_at=record["created_at"]
            )
            for record in records
        ]

    @staticmethod
    async def get_present_count_today(today_date: str) -> int:
        """Get count of employees present today"""
        db = get_db()
        count = await db["attendance"].count_documents({
            "date": today_date,
            "status": "Present"
        })
        return count

    @staticmethod
    async def get_total_attendance() -> int:
        """Get total attendance records"""
        db = get_db()
        return await db["attendance"].count_documents({})

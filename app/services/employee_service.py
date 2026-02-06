from datetime import datetime
from fastapi import HTTPException, status
from app.database import get_db
from app.schemas.employee_schema import EmployeeCreate, EmployeeResponse
from app.utils.validators import validate_email, generate_employee_id


class EmployeeService:
    """Service for employee operations"""

    @staticmethod
    async def create_employee(employee_data: EmployeeCreate) -> EmployeeResponse:
        """Create a new employee"""
        db = get_db()
        
        # Validate email
        if not validate_email(employee_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        
        # Check if email already exists
        existing_email = await db["employees"].find_one({"email": employee_data.email})
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )
        
        # Generate unique employee ID
        count = await db["employees"].count_documents({})
        employee_id = generate_employee_id(count)
        
        # Create employee document
        employee_doc = {
            "employee_id": employee_id,
            "full_name": employee_data.full_name,
            "email": employee_data.email,
            "department": employee_data.department,
            "created_at": datetime.utcnow()
        }
        
        result = await db["employees"].insert_one(employee_doc)
        
        return EmployeeResponse(
            employee_id=employee_id,
            full_name=employee_data.full_name,
            email=employee_data.email,
            department=employee_data.department,
            created_at=employee_doc["created_at"]
        )

    @staticmethod
    async def get_all_employees() -> list[EmployeeResponse]:
        """Get all employees"""
        db = get_db()
        employees = await db["employees"].find().sort("created_at", -1).to_list(None)
        
        return [
            EmployeeResponse(
                employee_id=emp["employee_id"],
                full_name=emp["full_name"],
                email=emp["email"],
                department=emp["department"],
                created_at=emp["created_at"]
            )
            for emp in employees
        ]

    @staticmethod
    async def get_employee_by_id(employee_id: str) -> EmployeeResponse:
        """Get employee by employee_id"""
        db = get_db()
        employee = await db["employees"].find_one({"employee_id": employee_id})
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee {employee_id} not found"
            )
        
        return EmployeeResponse(
            employee_id=employee["employee_id"],
            full_name=employee["full_name"],
            email=employee["email"],
            department=employee["department"],
            created_at=employee["created_at"]
        )

    @staticmethod
    async def delete_employee(employee_id: str) -> dict:
        """Delete employee and related attendance records"""
        db = get_db()
        
        # Check if employee exists
        employee = await db["employees"].find_one({"employee_id": employee_id})
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee {employee_id} not found"
            )
        
        # Delete employee
        await db["employees"].delete_one({"employee_id": employee_id})
        
        # Delete related attendance records
        await db["attendance"].delete_many({"employee_id": employee_id})
        
        return {"message": f"Employee {employee_id} deleted successfully"}

    @staticmethod
    async def get_total_employees() -> int:
        """Get total number of employees"""
        db = get_db()
        return await db["employees"].count_documents({})

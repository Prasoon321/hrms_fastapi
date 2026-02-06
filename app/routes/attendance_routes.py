from fastapi import APIRouter, status
from app.schemas.attendance_schema import AttendanceCreate, AttendanceResponse
from app.services.attendance_service import AttendanceService

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post(
    "/",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Mark attendance"
)
async def mark_attendance(attendance_data: AttendanceCreate):
    """
    Mark attendance for an employee with the following details:
    - employee_id: ID of the employee (e.g., EMP001)
    - date: Date in YYYY-MM-DD format
    - status: One of Present, Absent, Half Day, Leave
    """
    return await AttendanceService.mark_attendance(attendance_data)


@router.get(
    "/",
    summary="Get all attendance records"
)
async def get_all_attendance():
    """
    Retrieve all attendance records.
    Returns records sorted by date in descending order.
    Includes employee names joined from employee collection.
    """
    records = await AttendanceService.get_all_attendance()
    return {"records": records, "total": len(records)}


@router.get(
    "/{employee_id}",
    response_model=list[AttendanceResponse],
    summary="Get attendance records for an employee"
)
async def get_employee_attendance(employee_id: str):
    """
    Get all attendance records for a specific employee.
    Example: /attendance/EMP001
    """
    return await AttendanceService.get_attendance_by_employee(employee_id)

from fastapi import APIRouter, status
from app.schemas.employee_schema import EmployeeCreate, EmployeeResponse, EmployeeList
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee"
)
async def create_employee(employee_data: EmployeeCreate):
    """
    Create a new employee with the following details:
    - full_name: Employee's full name
    - email: Unique email address
    - department: Department name
    """
    return await EmployeeService.create_employee(employee_data)


@router.get(
    "/",
    response_model=list[EmployeeResponse],
    summary="Get all employees"
)
async def get_all_employees():
    """
    Retrieve all employees from the system.
    Returns a list of all employees sorted by creation date.
    """
    return await EmployeeService.get_all_employees()


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    summary="Get employee by ID"
)
async def get_employee(employee_id: str):
    """
    Get a specific employee by their employee_id.
    Example: /employees/EMP001
    """
    return await EmployeeService.get_employee_by_id(employee_id)


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an employee"
)
async def delete_employee(employee_id: str):
    """
    Delete an employee and their associated attendance records.
    Example: /employees/EMP001
    """
    return await EmployeeService.delete_employee(employee_id)

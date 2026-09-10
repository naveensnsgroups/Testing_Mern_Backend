from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator
import re
from datetime import datetime

GenderEnum = Literal['Male', 'Female', 'Other', '']
DepartmentEnum = Literal['IT', 'HR', 'Finance', 'Marketing', 'Operations', 'Sales', 'Admin', 'Other', '']

class EmployeeCreateUpdate(BaseModel):
    fullName: str = Field(..., max_length=100, description="Full name must contain only letters and spaces")
    employeeId: str = Field(..., max_length=20, description="Employee ID must start with EMP followed by numbers")
    email: str = Field(..., max_length=150, description="Email must end with @snsgroups.com")
    phone: str = Field(..., max_length=10, description="Phone number must be exactly 10 digits")
    dateOfBirth: Optional[str] = None
    gender: Optional[GenderEnum] = None
    address: Optional[str] = Field(None, max_length=500)
    department: Optional[DepartmentEnum] = None
    position: Optional[str] = Field(None, max_length=100)
    joinDate: Optional[str] = None

    @field_validator('fullName')
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('Full name is required')
        if not re.match(r'^[A-Za-z\s]+$', v):
            raise ValueError('Full name must contain only letters and spaces (no numbers or special characters)')
        return v

    @field_validator('employeeId')
    @classmethod
    def validate_employee_id(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('Employee ID is required')
        if not re.match(r'^EMP\d+$', v):
            raise ValueError('Employee ID must start with capital EMP followed by numbers (e.g. EMP001)')
        return v

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.strip().lower()
        if not v:
            raise ValueError('Email is required')
        if not re.match(r'^[a-z0-9._%+-]+@snsgroups\.com$', v):
            raise ValueError('Email must be in lowercase and end with @snsgroups.com domain')
        return v

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('Phone number is required')
        if not re.match(r'^\d{10}$', v):
            raise ValueError('Phone number must be exactly 10 digits (numbers only)')
        return v

    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v: Optional[str]) -> Optional[str]:
        if v == '':
            return None
        return v

    @field_validator('department')
    @classmethod
    def validate_department(cls, v: Optional[str]) -> Optional[str]:
        if v == '':
            return None
        return v


def employee_helper(employee) -> dict:
    if not employee:
        return {}
    
    result = {
        "_id": str(employee["_id"]),
        "fullName": employee.get("fullName"),
        "employeeId": employee.get("employeeId"),
        "email": employee.get("email"),
        "phone": employee.get("phone"),
        "dateOfBirth": employee.get("dateOfBirth"),
        "gender": employee.get("gender"),
        "address": employee.get("address"),
        "department": employee.get("department"),
        "position": employee.get("position"),
        "joinDate": employee.get("joinDate"),
    }
    
    if "createdAt" in employee:
        created_at = employee["createdAt"]
        if isinstance(created_at, datetime):
            result["createdAt"] = created_at.isoformat()
        else:
            result["createdAt"] = created_at

    if "updatedAt" in employee:
        updated_at = employee["updatedAt"]
        if isinstance(updated_at, datetime):
            result["updatedAt"] = updated_at.isoformat()
        else:
            result["updatedAt"] = updated_at

    return result

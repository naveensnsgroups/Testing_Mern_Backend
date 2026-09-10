from fastapi import APIRouter, Query, HTTPException, status
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError
from datetime import datetime
from typing import Optional

from app.database import get_employee_collection
from app.schemas.employee import EmployeeCreateUpdate, employee_helper

router = APIRouter(prefix="/api/employees", tags=["Employees"])

ALLOWED_FIELDS = [
    'fullName', 'employeeId', 'email', 'phone',
    'dateOfBirth', 'gender', 'address',
    'department', 'position', 'joinDate',
]

def pick_fields(data: dict) -> dict:
    safe_data = {}
    for key in ALLOWED_FIELDS:
        val = data.get(key)
        if val is not None:
            if isinstance(val, str):
                trimmed = val.strip()
                safe_data[key] = trimmed.lower() if key == 'email' else trimmed
            else:
                safe_data[key] = val
    return safe_data

def is_valid_object_id(id_str: str) -> bool:
    return ObjectId.is_valid(id_str)


@router.get("", response_model=None)
async def get_all_employees(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100)
):
    try:
        collection = get_employee_collection()
        skip = (page - 1) * limit

        cursor = collection.find().sort("createdAt", -1).skip(skip).limit(limit)
        employees_cursor = await cursor.to_list(length=limit)
        total = await collection.count_documents({})

        employees = [employee_helper(emp) for emp in employees_cursor]

        pages = (total + limit - 1) // limit if limit > 0 else 0

        return {
            "success": True,
            "count": len(employees),
            "total": total,
            "page": page,
            "pages": pages,
            "data": employees,
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.get("/{id}", response_model=None)
async def get_employee_by_id(id: str):
    if not is_valid_object_id(id):
        raise HTTPException(
            status_code=400,
            detail={"success": False, "message": "Invalid employee ID format"}
        )

    try:
        collection = get_employee_collection()
        employee = await collection.find_one({"_id": ObjectId(id)})
        if not employee:
            raise HTTPException(
                status_code=404,
                detail={"success": False, "message": "Employee not found"}
            )

        return {"success": True, "data": employee_helper(employee)}
    except HTTPException as he:
        raise he
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.post("", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_employee(payload: EmployeeCreateUpdate):
    try:
        collection = get_employee_collection()
        safe_data = pick_fields(payload.model_dump())
        
        now = datetime.utcnow()
        safe_data["createdAt"] = now
        safe_data["updatedAt"] = now

        result = await collection.insert_one(safe_data)
        created_employee = await collection.find_one({"_id": result.inserted_id})

        return {
            "success": True,
            "message": "Employee created successfully",
            "data": employee_helper(created_employee),
        }
    except DuplicateKeyError as dke:
        details = str(dke.details) if hasattr(dke, 'details') else str(dke)
        field_name = "Field"
        if "employeeId" in details:
            field_name = "employeeId"
        elif "email" in details:
            field_name = "email"
        raise HTTPException(
            status_code=409,
            detail={"success": False, "message": f"{field_name} already exists"}
        )
    except HTTPException as he:
        raise he
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.put("/{id}", response_model=None)
async def update_employee(id: str, payload: EmployeeCreateUpdate):
    if not is_valid_object_id(id):
        raise HTTPException(
            status_code=400,
            detail={"success": False, "message": "Invalid employee ID format"}
        )

    try:
        collection = get_employee_collection()
        safe_data = pick_fields(payload.model_dump())
        safe_data["updatedAt"] = datetime.utcnow()

        updated_employee = await collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": safe_data},
            return_document=True
        )

        if not updated_employee:
            raise HTTPException(
                status_code=404,
                detail={"success": False, "message": "Employee not found"}
            )

        return {
            "success": True,
            "message": "Employee updated successfully",
            "data": employee_helper(updated_employee),
        }
    except DuplicateKeyError as dke:
        details = str(dke.details) if hasattr(dke, 'details') else str(dke)
        field_name = "Field"
        if "employeeId" in details:
            field_name = "employeeId"
        elif "email" in details:
            field_name = "email"
        raise HTTPException(
            status_code=409,
            detail={"success": False, "message": f"{field_name} already exists"}
        )
    except HTTPException as he:
        raise he
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.delete("/{id}", response_model=None)
async def delete_employee(id: str):
    if not is_valid_object_id(id):
        raise HTTPException(
            status_code=400,
            detail={"success": False, "message": "Invalid employee ID format"}
        )

    try:
        collection = get_employee_collection()
        deleted_employee = await collection.find_one_and_delete({"_id": ObjectId(id)})

        if not deleted_employee:
            raise HTTPException(
                status_code=404,
                detail={"success": False, "message": "Employee not found"}
            )

        return {"success": True, "message": "Employee deleted successfully"}
    except HTTPException as he:
        raise he
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

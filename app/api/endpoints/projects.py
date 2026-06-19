from fastapi import APIRouter, status
from typing import Annotated
from fastapi.params import Depends
from app.core.security import get_current_user
from app.schemas.user import InDbUser
from app.schemas.project import Project
from app.db.simple_db import projects_db
from uuid import uuid4
router = APIRouter()

@router.post("/projects", status_code=status.HTTP_201_CREATED)
def create_projects(
        project: Project,
        current_user: Annotated[InDbUser ,Depends(get_current_user)]
):
    project_id = str(uuid4())
    projects_db[project_id] = {
        "project_name": project.name,
        "project_id": project_id,
        "description": project.description,
        "owner": current_user.username,
        "owner_id": current_user.id,
        "role": "owner",
        "members": {},
        "documents": []
    }
    return {"created project": project.name}

@router.get("/projects", status_code=status.HTTP_200_OK)
def get_projects(current_user: Annotated[InDbUser ,Depends(get_current_user)]):
    # return only projects where we are the owner for now
    user_projects = [v for k,v in projects_db.items() if (v["owner"] ==
                                                            current_user.username)]
    return user_projects

@router.get("/projects/{project_id}/info ")
def project_info(project_id: int):
    return {"project_info-get": "to be implemented"}

@router.put("/projects/{project_id}/info ")
def project_info(project_id: int):
    return {"project_info-put": "to be implemented"}

@router.delete("/projects/{project_id} ")
def delete_project(project_id: int):
    return {"project-delete": "to be implemented"}

@router.get("/projects/{project_id}/documents")
def project_documents(project_id: int):
    return {"project_documents-get": "to be implemented"}

@router.post("/projects/{project_id}/documents")
def project_documents(project_id: int):
    return {"project_documents-post": "to be implemented"}


@router.post("/projects/{project_id}/invite?user=<login>")
def invite_user(project_id: int):
    return {"invite_user-post": "to be implemented"}

@router.get("/projects/{project_id}/share?with=<email>")
def send_join_link(project_id: int):
    return {"send_join_link-get": "to be implemented"}
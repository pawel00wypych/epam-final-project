from fastapi import APIRouter

router = APIRouter()

@router.post("/projects")
def projects():
    return {"projects-post": "to be implemented"}

@router.get("/projects")
def projects():
    return {"projects-get": "to be implemented"}

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
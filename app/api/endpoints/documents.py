from fastapi import APIRouter

router = APIRouter()

@router.get("/document/{document_id}")
def document(document_id: int):
    return {"document-get": "to be implemented"}

@router.put("/document/{document_id}")
def document(document_id: int):
    return {"document-put": "to be implemented"}

@router.delete("/document/{document_id}")
def document(document_id: int):
    return {"document-delete": "to be implemented"}
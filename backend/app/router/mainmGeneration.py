from fastapi import APIRouter, status, HTTPException


router = APIRouter(
    prefix="/api/manimGeneration"
)


@router.get("/")
def hello():
    return {"data":"hello World"}

@router.post("/" status_code=)
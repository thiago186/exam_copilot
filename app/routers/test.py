from fastapi import APIRouter

router = APIRouter(
    prefix="/test",
    tags=["test"],
)

@router.get("/helloworld")
async def hello_world():
    return {"message": "Hello World"}
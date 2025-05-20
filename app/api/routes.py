from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello from W1 Hackathon Backend 💖"}

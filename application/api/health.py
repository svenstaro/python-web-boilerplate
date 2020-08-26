""" health check endpoint for example for k8s health checks """
from fastapi import APIRouter

router = APIRouter()

@router.get("/health", response_model=str)
async def health_check():
    return "Healthy!"


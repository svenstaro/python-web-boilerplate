""" health check endpoint for example for k8s health checks """
from fastapi import APIRouter, Depends
from application import get_config


router = APIRouter()


@router.get("/health", response_model=str)
async def health_check(config: str = Depends(get_config)):
    print(f"{config}")
    return "Healthy!"


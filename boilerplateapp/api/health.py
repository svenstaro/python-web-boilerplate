""" health check endpoint for example for k8s health checks """
from fastapi import APIRouter, Depends
from boilerplateapp import get_config


router = APIRouter()


@router.get("/health", response_model=str)
async def health_check(config: str = Depends(get_config)):
    return "Healthy!"


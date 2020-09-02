""" module for user intarcation """
from application.storage.user import Users, UserInput, UserOutput
from application.hasher import hasher
from fastapi import APIRouter
from typing import Optional
import logging



router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register", response_model=bool)
async def register_user(usr: UserInput):
    """ 
    # Add a new userto the db
    ---
    ## Input:
    - UserInput
    ## Output:
    - bool: True if registration was succesful, False otherwise
    """
    try:
        await Users(name=usr.name, pwhash=hasher.hash(f"{usr.name}{usr.password}")).save()
        return True
    except Exception as ex:
        logger.error(f"Could not save usr due to {ex}")
        return False



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
    await Users(name=usr.name, pwhash=usr.password).save()
    # try:
    #     new_usr = User(name=usr.name, pwhash=hasher.hash(f"{usr.name}{usr.password}"))
    #     print(new_usr)
    #     res = await new_usr.save()
    #     logger.info(res)
    #     return True if res is not None else False
    # except Exception as ex:
    #     logger.error(f"Could not save usr due to {ex}")
    #     return False



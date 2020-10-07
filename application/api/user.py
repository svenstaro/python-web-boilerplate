""" module for user intarcation """
from application.storage.user import User, UserInput, UserOutput
from application.hasher import get_hash, verify
# from application.storage.token import UserTokens, Token
from fastapi import APIRouter, HTTPException
from typing import Optional
from fastapi.logger import logger
import logging
import datetime 
from datetime import timedelta
import uuid

router = APIRouter()
logger.setLevel(logging.DEBUG)


@router.on_event("startup")
async def startup():
    await User.__database__.connect()

@router.on_event("shutdown")
async def shutdown():
    await User.__database__.close()


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
        await User.objects.create(name=usr.name, pwhash=await get_hash(usr))
        return True
    except Exception as ex:
        logger.error(f"Could not save usr due to {ex}")
        return False


# @router.post("/test")
# async def test(usr: UserInput, origin: str):
#     now = datetime.datetime.now()
#     eu = await Users.filter(name=usr.name).first()
#     token = await UserTokens.create(usr=eu.id, token_id=str(uuid.uuid4()),
#             expiry=now+datetime.timedelta(days=1),
#             access_origin=origin)
#     return True
#
#
# @router.post("/auth", response_model=bool)
# async def login(usr: UserInput, access_origin: str):
#     """
#     # Login existing user
#     ---
#     For existing user if the data is correct refresh access token
#     
#     ## Input: 
#     - UserInput: (usr_name, password)
#     - AccessOrigin: str identifyer of the browser/request origin
#     
#     ## Output:
#     - Token: str access_token (JWT)
#     """
#     # get existing user, get id, check for token for this origin, refresh if needed
#     now = datetime.datetime.now()
#     try:
#         exist_usr = await Users.filter(name=usr.name).first()
#         if exist_usr is not None and exist_usr.verify(usr.name):
#             # check for token, create/update if needed
#             try:
#                 tkn = await UserTokens.filter(usr_id=exist_usr.id, access_origin=access_origin).first()
#                 if tkn is not None:
#                     # expired token
#                     await tkn.update(expiry=now + timedelta(days=7))
#                     # return Token(token_id=tkn.token_id, access_origin=access_origin)
#                     return True
#                 else:
#                     # create token
#                     token = UserTokens(usr_id=exist_usr.id, access_origin=access_origin)
#                     await token.save()
#                     return False
#                     # return Token(token_id=token.token_id, access_origin=access_origin)
#             except Exception as ex:
#                 logger.error(f"Could not fetch/create token due to {ex}")
#                 return HTTPException(status_code=500, detail="problems with creating/getting token")
#         else:
#             # this is wrong password for existing user
#             logger.warning(f"user: {usr.name} has given wrong password")
#             return HTTPException(status_code=403, detail="user can not be logged in")
#     except Exception as ex:
#         logger.error(f"could not fetch user due to {ex}")
#         return HTTPException(status_code=500, detail="no user fetched")
#
#     
#     
#
#
# @router.get("/whoami", response_model=Optional[UserOutput])
# async def whoami():
#     return None
#
# @router.delete("/delete/{token}", response_model=bool)
# def delete_me():
#     return True

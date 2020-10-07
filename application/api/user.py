""" module for user intarcation """
from application.storage.user import User, UserInput, UserOutput
from application.hasher import get_hash, verify
from application.storage.token import UserTokens, Token
from fastapi import APIRouter, HTTPException
from typing import Optional
from fastapi.logger import logger
import logging
import datetime 
from datetime import timedelta
import uuid

router = APIRouter()
logger.setLevel(logging.DEBUG)


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


@router.post("/auth", response_model=bool)
async def login(usr: UserInput, access_origin: str):
    """
    # Login existing user
    ---
    For existing user if the data is correct refresh access token

    ## Input: 
    - UserInput: (usr_name, password)
    - AccessOrigin: str identifyer of the browser/request origin

    ## Output:
    - Token: str access_token (JWT)
    """
    # get existing user, get id, check for token for this origin, refresh if needed
    now = datetime.datetime.now()
    try:
        exist_usr = await User.objects.get(name=usr.name)
        print(f"{exist_usr.id} under {exist_usr.name}")
        if exist_usr is not None and await verify(exist_usr, usr):
            # check for token, create/update if needed
            try:
                # TODO: it looks like a bug or unfinished implementation:
                # https://github.com/encode/orm/blob/0eb84cb96c4f876997c7f2d340ede1723788a8e1/orm/models.py#L237
                tkn = await UserTokens.objects.filter(usr=exist_usr.id, access_origin=access_origin).all()
                if bool(tkn):
                    # expired token
                    await tkn[0].update(expiry=now + timedelta(days=7))
                    # return Token(token_id=tkn.token_id, access_origin=access_origin)
                    return True
                else:
                    # create token
                    token = await UserTokens.objects.create(usr=exist_usr, 
                            token_id=str(uuid.uuid4()),
                            expiry=now+datetime.timedelta(days=1),
                            access_origin=access_origin)
                    return False
                    # return Token(token_id=token.token_id, access_origin=access_origin)
            except Exception as ex:
                logger.error(f"Could not fetch/create token due to {ex}")
                return HTTPException(status_code=500, detail="problems with creating/getting token")
        else:
            # this is wrong password for existing user
            logger.warning(f"user: {usr.name} has given wrong password")
            return HTTPException(status_code=403, detail="user can not be logged in")
    except Exception as ex:
        logger.error(f"could not fetch user due to {ex}")
        return HTTPException(status_code=500, detail="no user fetched")
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

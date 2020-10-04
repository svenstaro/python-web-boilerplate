""" module for user intarcation """
from application.storage.user import Users, UserInput, UserOutput
from application.storage.token import UserTokens, Token
from fastapi import APIRouter, HTTPException
from typing import Optional
import logging
import datetime 
from datetime import timedelta


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
        usr = Users(usr=usr)
        await usr.save()
        return True
    except Exception as ex:
        logger.error(f"Could not save usr due to {ex}")
        return False

# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

@router.get("/auth", response_model=Token)
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
        exist_usr = await Users.filter(name=usr.name)
        if exist_usr is not None and exist_usr.verify(usr.name):
            # check for token, create/update if needed
            try:
                tkn = await UserTokens.filter(usr_id=exist_usr.id, access_origin=access_origin)
                if tkn is not None:
                    # expired token
                    await tkn.update(expiry=now + timedelta(days=7))
                    return Token(tkn.token_id, access_origin)
                else:
                    # create token
                    token = await UserTokens(usr_id=exist_usr.id, access_origin=access_origin)
                    return Token(token.token_id, access_origin)
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

    
    


@router.get("/whoami", response_model=Optional[UserOutput])
async def whoami():
    return None

@router.delete("/delete/{token}", response_model=bool)
def delete_me():
    return True

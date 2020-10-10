""" module for user intarcation """
from application.storage.user import User, UserInput, UserOutput
from application.hasher import get_hash, verify
from application.storage.token import UserTokens, Token
from fastapi import APIRouter, HTTPException, Request, Header
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
        await User.objects.create(name=usr.name, pwhash=get_hash(usr))
        return True
    except Exception as ex:
        logger.error(f"Could not save usr due to {ex}")
        return False


@router.post("/auth", response_model=Optional[Token])
async def auth(usr: UserInput, access_origin: str):
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
        if exist_usr is not None and verify(exist_usr, usr):
            # check for token, create/update if needed
            try:
                # TODO: it looks like a bug or unfinished implementation:
                # https://github.com/encode/orm/blob/0eb84cb96c4f876997c7f2d340ede1723788a8e1/orm/models.py#L237
                tkn = await UserTokens.objects.filter(usr=exist_usr.id, access_origin=access_origin).all()
                if bool(tkn):
                    # update token expiry
                    access_token = tkn[0].token
                    await tkn[0].update(expiry=now + timedelta(days=7))
                else:
                    # create token
                    access_token = str(uuid.uuid4())
                    token = await UserTokens.objects.create(usr=exist_usr, 
                            token=access_token,
                            expiry=now+datetime.timedelta(days=1),
                            access_origin=access_origin)
                    # return Token(token_id=token.token_id, access_origin=access_origin)
                return Token(token=access_token)
            except Exception as ex:
                logger.error(f"Could not fetch/create token due to {ex}")
                return None
        else:
            # this is wrong password for existing user
            logger.error(f"user: {usr.name} has given wrong password")
            raise HTTPException(status_code=403, detail="user can not be authenticated")
    except Exception as ex:
        logger.error(f"could not fetch user due to {ex}")
        return None


@router.get("/whoami", response_model=UserOutput)
async def whoami(request: Request, auth_token: str = Header(...)):
    """
    Return user for currently valid token/access_origin if any

    ## Params:
    - in header "auth-token" str token for a specific user

    ## Return:
    - UserOutput if token is applicable

    """
    now = datetime.datetime.now()
    try:
        usrtkn = await UserTokens.objects.get(token=auth_token)
        try:
            usr = await User.objects.get(id=usrtkn.usr)
        except Exception as ex:
            logger.error(f"no user found for id: {usrtkn.usr}")
            return UserOutput()
        status = usrtkn.expiry >= now
        return UserOutput(name=usr.name, token_status=status)
    except Exception as ex:
        logger.error(f"no user collected for provided token: {auth_token}")
        raise HTTPException(404, detail="No such token")


@router.delete("/delete", response_model=bool)
async def delete_me(usr: UserInput):
    """
    Delete this user
    ---
    with all credentials correct the user can hard delete his record

    ## Params:
    - UserInput json object containing username and password

    ## Return:
    True if succesful, False otherwise
    """
    try:
        exist_usr = await User.objects.get(name=usr.name)
        if exist_usr:
            valid = verify(exist_usr, usr)
            if valid:
                # TODO: need to check more in depth if cascade delete is implemented
                tokens = await UserTokens.objects.filter(usr=exist_usr.id).all()
                # TODO: to asynchronize this code
                for t in tokens:
                    await t.delete()
                await exist_usr.delete()
                return True
    except Exception as ex:
        logger.error(f"could not delete user due to {ex}")
        return False

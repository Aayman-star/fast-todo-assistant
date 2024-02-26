import os
from dotenv import load_dotenv,find_dotenv
from datetime import timedelta,datetime
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine,User,UserCreate,Token
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm   
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware



load_dotenv(override=True)
dotenv_file = find_dotenv()
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
print(JWT_SECRET_KEY)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]	
)

ALGORITHM = os.environ["ALGORITHM"]

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer =  OAuth2PasswordBearer(tokenUrl="auth/token")

# Dependency
def get_session():
    with Session(engine) as session:
        yield session

#db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/",status_code=status.HTTP_201_CREATED,response_model = User)
async def create_user(*,session:Session = Depends(get_session), user: UserCreate):
    """Create a new user"""
    user_model = UserCreate(username=user.username,useremail=user.useremail, password=password_context.hash(user.password))
    user_item = User.model_validate(user_model)
    if not user_item:
        raise HTTPException(status_code=400, detail="Invalid user data")
    session.add(user_item)
    session.commit()
    session.refresh(user_item)
    return user_item
  

@router.post("/token", response_model=Token)
async def login_for_access_token(*,session : Session = Depends(get_session),form_data: Annotated[OAuth2PasswordRequestForm , Depends()] ):
    """ this is where we send the acquired user data to be authenticated"""
    auth_user = authenticate_user(form_data.username,form_data.password, session)    
    print(auth_user)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
           )
    token = create_access_token(auth_user.username, auth_user.id,timedelta(minutes=20))
    if token:
        return{"access_token":token,"token_type":"bearer"}
    else:
        return "something is wrong"


def authenticate_user(username: str, password: str, session : Session = Depends(get_session)):
    user = session.query(User).filter(User.username == username).first()
    print(user)
    if not user:
        return False
    if not password_context.verify(password, user.password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    """This is where the jwt token in being created"""
    encode = {"sub": username, "id": user_id}
    expire = datetime.utcnow() + expires_delta
    encode.update({"exp": expire})
    return jwt.encode(encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """This is where we access the information about the current user"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="could not validate the user")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="could not validate the user")

from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
from models import user_data, bonus_tiers
from schemas import UserModel

app = FastAPI()

# Конфигурация JWT
SECRET_KEY = "secret_key"
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Класс для работы с токенами
class TokenManager:
    @staticmethod
    def generate_token(data: dict, expires_delta: timedelta = None):
        expiration = datetime.utcnow() + (expires_delta or timedelta(minutes=TOKEN_EXPIRE_MINUTES))
        token = jwt.encode({**data, "exp": expiration}, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token

@app.post("/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_data.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    access_token = TokenManager.generate_token({"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username not in user_data:
            raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
        return UserModel(**user_data[username])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})

@app.get("/bonus", response_model=dict)
async def get_bonus_info(current_user: UserModel = Depends(get_current_user)):
    user_spending = current_user.spending
    eligible_levels = sorted(bonus_tiers, key=lambda x: x["min_spending"])
    current_tier = next((tier for tier in reversed(eligible_levels) if user_spending >= tier["min_spending"]), None)
    next_tier = next((tier for tier in eligible_levels if user_spending < tier["min_spending"]), "No higher level")
    return {"current_tier": current_tier, "next_tier": next_tier}

@app.middleware("http")
async def validate_token(request: Request, call_next):
    if request.url.path.startswith("/bonus"):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return Response("Authorization token missing", status_code=401)
        token = token.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            username = payload.get("sub")
            if username not in user_data:
                return Response("Invalid token", status_code=401)
        except JWTError:
            return Response("Invalid token", status_code=401)

    response = await call_next(request)
    return response

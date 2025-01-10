from pydantic import BaseModel

# Модель для пользователя
class UserModel(BaseModel):
    username: str
    password: str
    spending: float

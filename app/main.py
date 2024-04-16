import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from database.engine import get_db
from database.security import pwd_context, oauth2_scheme, get_current_user
from database.user import User
from fastapi import FastAPI, HTTPException, Depends, Body
from jose import JWTError, jwt

app = FastAPI()

load_dotenv()

secret_key = os.getenv("SECRET_KEY")

# Роут для регистрации пользователя
@app.post("/register/")
async def register_user(
        username: str = Body(..., embed=True),
        fullname: str = Body(..., embed=True),
        password: str = Body(..., embed=True),
        db: Session = Depends(get_db)
):
    # Хэширование пароля перед сохранением
    hashed_password = pwd_context.hash(password)
    user = User(name=username, fullname=fullname, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Роут для входа пользователя
@app.post("/login/")
async def login_user(
        username: str = Body(..., embed=True),
        password: str = Body(..., embed=True),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.name == username).first()
    if user and pwd_context.verify(password, user.hashed_password):
        # Генерация токена
        token_data = {"sub": username}
        token = jwt.encode(token_data, secret_key, algorithm="HS256")
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.put("/change-password/", tags=["User"])
async def change_password(
        new_password: str = Body(..., embed=True),
        current_user: User = Depends(get_current_user),
        current_db: Session = Depends(get_db)
):
    # Проверка существования пользователя
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Обновление пароля пользователя
    current_user.hashed_password = pwd_context.hash(new_password)
    current_user.updated_at = datetime.utcnow()

    current_db.commit()
    current_db.refresh(current_user)
    return {"message": "Password updated successfully"}


# Генерация OpenAPI JSON спецификации
openapi_schema = app.openapi()

# Запуск сервера
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

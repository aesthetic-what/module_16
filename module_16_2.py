from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()


@app.get("/")
async def main():
    return {"message": "Главная страница"}


@app.get("/users/admin")
async def admin():
    return {"message": "Вы вошли как админ"}


@app.get("/users/{user_id}")
async def user(
    user_id: Annotated[int, Path(ge=1, le=100, description="Enter user ID", example=1)]
):
    return {"message": f"Вы вошли как пользователь № {user_id}"}


@app.get("/users/{username}/{age}")
async def full_user(
    username: Annotated[
        str, Path(min_length=5, max_length=20, description="Введите свое имя", example="Timur")
    ],
    age: Annotated[
        int, Path(ge=18, le=120, description="Введите свой возраст", example=18)
    ],
):
    return {'about': f'Ваше имя: {username}, Ваш возраст: {age}'}

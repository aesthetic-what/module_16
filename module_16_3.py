from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = [{'id': 1, 'name': 'Timur', 'age': 18}]

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

@app.get('/users')
async def get_users():
    return users


@app.post("/users/{username}/{age}")
async def full_user(
    username: Annotated[
        str, Path(min_length=5, max_length=20, description="Введите свое имя", example="Timur")
    ],
    age: Annotated[
        int, Path(ge=18, le=120, description="Введите свой возраст", example=18)
    ],
):
    new_id = max(user['id'] for user in users) + 1 if users else 1
    new_user = {'id': new_id, 'username': username, 'age': age}
    users.append(new_user)
    return new_user


@app.put("/users/{users_id}/{username}/{age}")
async def update_user(user_id: int,
    username: Annotated[
        str, Path(min_length=5, max_length=20, description="Введите свое имя", example="Timur")
    ],
    age: Annotated[
        int, Path(ge=18, le=120, description="Введите свой возраст", example=18)
    ],
):
    for user in users:
        if user['id'] == user_id:
            user['username'] = username
            user['age'] = age
            return user
        
@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user['id'] == user_id:
            del users[i]
            return {'details': f'Пользователь № {user_id} удален'}
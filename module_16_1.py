from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def main():
    return {"message": 'Главная страница'}

@app.get("/users/admin")
async def admin():
    return {"message": "Вы вошли как админ"}

@app.get("/users/{user_id}")
async def user(user_id: int):
    return {"message": f"Вы вошли как пользователь № {user_id}"}

@app.get("/users")
async def full_user(username: str, age: int):
    return {"Инфомация о пользователе": f"Имя: {username}, Возраст: {age}"}
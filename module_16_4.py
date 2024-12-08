from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel, Field

app = FastAPI()

# users = [{'id': 1, 'name': 'Timur', 'age': 18}]

class User(BaseModel):
    user_id: int
    username: str
    age: int

class UserCreate(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    age: int = Field(ge=18, le=120)

users: List[User] = [
    User(user_id=1, username='Timur', age='18')
]

@app.get("/")
async def main():
    return {"message": "Главная страница"}

@app.get('/users', response_model=List[User])
async def get_users():
    return users

@app.post("/users/{username}/{age}", response_model=User)
async def full_user(user: UserCreate):
    new_id = max((u.user_id for u in users), default=0) + 1
    new_user = User(user_id=new_id, username=user.username, age=user.age)
    users.append(new_user)
    return new_user

@app.put("/users/{user_id}/{username}/{age}", response_model=User)
async def update_user(user_id: int, user: UserCreate):
    for u in users:
        if u.user_id == user_id:
            u.username = user.username
            u.age = user.age
            return u
    raise HTTPException(status_code=404, detail='Пользователь не найден')
        
@app.delete('/users/{user_id}', response_model=dict)
async def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.user_id == user_id:
            del users[i]
            return {'details': f'Пользователь № {user_id} удален'}
    raise HTTPException(status_code=404, detail='Пользователь не найден')
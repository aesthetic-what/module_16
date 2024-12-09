from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List
from pydantic import BaseModel, Field

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)
templates = Jinja2Templates(directory='templates')

# users = [{'id': 1, 'name': 'Timur', 'age': 18}]

class User(BaseModel):
    user_id: int
    username: str
    age: int

class UserCreate(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    age: int = Field(ge=18, le=120)

users: List[User] = [
    User(user_id=1, username='Timur', age='18'),
    User(user_id=2, username='Anton', age='18'),
    User(user_id=3, username='Egor', age='18'),
    User(user_id=4, username='Andrey', age='18')
]

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/users", response_model=List[User])
async def get_all_users():
    return users

@app.get('/users/{user_id}', response_class=HTMLResponse)
async def get_users(request: Request, user_id: int):
    user = next((user for user in users if user.user_id == user_id), None)
    if not user:
        return HTMLResponse(status_code=404, detail='Пользователь не найден')
    return templates.TemplateResponse("users.html", {"request": request, "user": user})

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
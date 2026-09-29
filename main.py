from fastapi import FastAPI, HTTPException
from schemas import UserCreate, UserOut
from data_manager import DataManager
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/users", response_model=UserOut)
def create_user(user: UserCreate):
    message, new_user = DataManager().add_user(user)
    if message:
        raise HTTPException(status_code=400, detail=message)
    return new_user

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)


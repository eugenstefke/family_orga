from fastapi import FastAPI
import uvicorn
from routes.doctor_routes import router as doctor_router
from routes.user_routes import router as user_router
from routes.familymember_routes import router as familymember_router
app = FastAPI()
app.include_router(doctor_router, tags=["Doctor"])
app.include_router(user_router, tags=["User"])
app.include_router(familymember_router, tags=["Familymember"])

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)


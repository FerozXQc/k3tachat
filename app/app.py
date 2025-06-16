from fastapi import FastAPI  
from fastapi.middleware.cors import CORSMiddleware
from redis_client import refreshSessionMiddleware
import uvicorn
from auth_routes import auth_router

app = FastAPI()

app.add_middleware(refreshSessionMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router,prefix='/auth')

@app.get("/")
def read_root():
    return {"message": "Hello from K3tachat"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

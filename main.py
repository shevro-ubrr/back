from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from endpoints import router

app = FastAPI()
app.include_router(router)

origins = [
    'https://localhost',
    'https://localhost:3000',
    'https://localhost:8000',
    'https://front-cfi9jc2dh-wswfws-projects.vercel.app/',
    'https://*.vercel.app',
    'https://front-wswfws-projects.vercel.app/'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

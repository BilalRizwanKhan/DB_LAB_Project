from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import engine
import models, os
from routers import auth, properties, admin, favorites, reviews, inquiries, users, appointments

os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/avatars", exist_ok=True)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DreamHomes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(properties.router)
app.include_router(admin.router)
app.include_router(favorites.router)
app.include_router(reviews.router)
app.include_router(inquiries.router)
app.include_router(users.router)
app.include_router(appointments.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/static",  StaticFiles(directory="frontend"), name="static")

@app.get("/")
def root():
    return FileResponse("frontend/home.html")

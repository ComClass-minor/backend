from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017") #the second mongodb is the name of the service in the docker-compose file

db = client["community"]
 

# call the secret key
load_dotenv(os.path.join('core', '.env'))
SECRET_KEY = os.getenv("SECRET_KEY")
print(SECRET_KEY)
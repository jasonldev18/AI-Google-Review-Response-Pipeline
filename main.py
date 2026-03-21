from fastapi import FastAPI
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager


load_dotenv()

scheduler = BackgroundScheduler()

#handles startup and shutdown of app
@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

#google creds for GBP API call
client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

#endpoint that checks if app is running
@app.get("/health") 
async def root(): 
    return{"status": "running"}

#endpoint that allows manual trigger to fetch review
@app.post("/reviews/fetch")
async def fetch_reviews():
    return {"message": "fetch triggered"}


#test
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



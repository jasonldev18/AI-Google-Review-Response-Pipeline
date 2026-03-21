from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
import os
from contextlib import asynccontextmanager
from gbp import fetch_reviews, post_response
from datetime import datetime, timedelta, timezone
from analysis import analysis, extract_name
from llm import generate_response
from safety_check import safety_check
from log import log_entry, init_db



#runs pipeline
def process_reviews():

    try:
        reviews = fetch_reviews()
    except Exception as e:
        print(f"Failed to fetch review: {e}")
        return

    if not reviews:
        print("No new reviews found")
        return


    for review in reviews:
        review_time = datetime.fromisoformat(review['createTime'].replace("Z", "+00:00"))
        cutoff = datetime.now(timezone.utc) - timedelta(days=30)

        if review_time < cutoff or 'reviewReply' in review:
            continue

        if 'comment' not in review:
            continue

        analysis_result = analysis(review['comment'])
        reviewer_name = extract_name(review['reviewer']['displayName'])

        response = generate_response(analysis_result, reviewer_name)

        safety_result = safety_check(analysis_result, response)

        if safety_result['passed']:
            post_response(review['reviewId'], response)
            posting_method = 'auto'
        else:
            posting_method = 'draft'

    
        log_entry(review['reviewId'], review['comment'], review_time, analysis_result, response, safety_result['passed'], posting_method, datetime.now(timezone.utc))
    
    

scheduler = BackgroundScheduler()
scheduler.add_job(process_reviews, 'interval', hours = 24)

#handles startup and shutdown of app
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

#endpoint that checks if app is running
@app.get("/health") 
async def root(): 
    return{"status": "running"}

#endpoint that allows manual trigger to fetch review
@app.post("/reviews/fetch")
async def manual_fetch():
    process_reviews()
    return {"message": "fetch triggered"}




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)






import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS review_logs(
    review_id TEXT PRIMARY KEY,
    review_text TEXT,
    review_timestamp TIMESTAMPTZ,
    analysis TEXT,
    generated_response TEXT,
    safety_passed BOOL,
    posting_method TEXT,
    response_timestamp TIMESTAMPTZ
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def log_entry(review_id, review_text, review_timestamp, analysis, generated_response, safety_passed, posting_method, response_timestamp):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO review_logs VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s
    )""",
    (review_id, review_text, review_timestamp, json.dumps(analysis), generated_response, safety_passed, posting_method, response_timestamp)
    )
    conn.commit()
    cursor.close()
    conn.close()
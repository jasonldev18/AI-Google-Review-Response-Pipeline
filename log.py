import sqlite3
import json

#creates database, then creates table inside database 
def init_db():
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()                  
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS review_logs(
    review_id TEXT PRIMARY KEY,
    review_text TEXT,
    review_timestamp DATETIME,
    analysis TEXT,
    generated_response TEXT,
    safety_passed BOOL,
    posting_method TEXT,
    response_timestamp DATETIME 
    )
    """)         
    conn.commit()                           
    conn.close()                           


def log_entry(review_id, review_text, review_timestamp, analysis, generated_response, safety_passed, posting_method, response_timestamp):
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()                  
    cursor.execute("""
    INSERT INTO review_logs VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?
    )""",           
    (review_id, review_text, review_timestamp, json.dumps(analysis), generated_response, safety_passed, posting_method, response_timestamp)
    )         
    conn.commit()                           
    conn.close()  
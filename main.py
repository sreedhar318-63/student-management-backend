from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, students, ai
from database import Base, engine
from routers import auth, students

import models.user     
import models.student  
Base.metadata.create_all(bind=engine)

# Auto-migrate: Add email column if missing
import sqlite3
try:
    conn = sqlite3.connect("./kuppam.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'email' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN email VARCHAR(100)")
        conn.commit()
    
    # Auto-link the email to the existing 'sreedhar' user for testing
    cursor.execute("UPDATE users SET email = 'sreedharg728@gmail.com' WHERE username = 'sreedhar' AND email IS NULL")
    conn.commit()
    
    conn.close()
except Exception as e:
    print(f"Auto-migration failed: {e}")

app = FastAPI(title="Student Management API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(ai.router)
@app.get("/")
def root():
    return {"message": "Student API is running"}
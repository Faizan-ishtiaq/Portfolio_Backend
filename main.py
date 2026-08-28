from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your Vite dev URL
    allow_methods=["*"],
    allow_headers=["*"],
)


class Projects(BaseModel):
    title:str
    tagline:str
    demo_url:str
    github_url:str
    tech_stack:str
    video_url:str
    featured:bool


class Inquiries(BaseModel):
    full_name: str
    email: str
    subject: str = ""
    message_body: str
    

def get_db():
    conn=psycopg2.connect(
        host="localhost",
        database="mydb",
        user="postgres",
        password="5225"
    )

    cursor=conn.cursor(cursor_factory=RealDictCursor)
    try:
        yield cursor
    finally:
        conn.close()

@app.get("/projects")
def get_projects(cursor= Depends(get_db)):
    cursor.execute("SELECT * from projects")
    results=cursor.fetchall()
    return results


@app.post("/inquiries")
def create_project(inquiry:Inquiries,cursor= Depends(get_db)):
    cursor.execute("INSERT INTO inquiries(full_name,email,subject,message_body) VALUES (%s,%s,%s,%s)",(inquiry.full_name,inquiry.email,inquiry.subject,inquiry.message_body))
    cursor.connection.commit()
    return{"message":"project added successfully"}




    
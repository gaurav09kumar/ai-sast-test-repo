from fastapi import FastAPI, Request
import sqlite3
import os
import subprocess

app = FastAPI()

# ❌ Intentionally hard-coded secret for SAST testing
HARDCODED_API_KEY = "sk-test-INTENTIONALLY-INSECURE-123456"  # CWE-798, OWASP A02

DATABASE_PATH = "test.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn


@app.post("/search")
async def search(request: Request):
    body = await request.json()
    user_query = body.get("q", "")  # CWE-20 Improper Input Validation

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = f"SELECT * FROM items WHERE name LIKE '%{user_query}%';"  # CWE-89
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()

    return {"query": user_query, "results": results}


@app.post("/run")
async def run_command(request: Request):
    body = await request.json()
    cmd = body.get("cmd", "echo hello")

    output = subprocess.check_output(cmd, shell=True)  # CWE-78

    return {"cmd": cmd, "output": output.decode("utf-8")}


@app.get("/health")
async def health():
    return {"status": "ok"}

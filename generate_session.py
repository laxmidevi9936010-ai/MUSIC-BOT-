import os
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()
api_id = int(os.getenv("API_ID", "35828291"))
api_hash = os.getenv("API_HASH", "c025ee9d01d73b9d738d4f3e5e6137e2")

if not api_id or not api_hash:
    raise SystemExit("API_ID/API_HASH .env me daalo, phir run karo.")

with Client("assistant_session", api_id=api_id, api_hash=api_hash, in_memory=True) as app:
    print("\nASSISTANT_SESSION=", app.export_session_string(), "\n")

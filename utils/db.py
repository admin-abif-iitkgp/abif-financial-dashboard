# app.py
import streamlit as st
import os
from pymongo import MongoClient
from dotenv import load_dotenv


# Load environment variables and setup MongoDB
load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["financial_app"]
users = db.users
financial_data = db.financial_data

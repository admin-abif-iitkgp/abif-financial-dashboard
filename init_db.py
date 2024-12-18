# init_db.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URI'))
db = client['financial_app']
users = db.users

def create_admin():
    if not users.find_one({"username": "admin"}):
        password = "admin123"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        admin_user = {
            "username": "admin",
            "password": hashed_password.decode('utf-8'),
            "role": "admin"
        }
        users.insert_one(admin_user)
        print("Admin user created successfully!")

if __name__ == "__main__":
    create_admin()

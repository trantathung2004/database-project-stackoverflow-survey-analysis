import csv
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()
admin_id = 1
username = os.getenv("ADMIN_USERNAME")
password = os.getenv("ADMIN_PASSWORD")
role = os.getenv("ADMIN_ROLE")


SECRET_KEY = '' 
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
hashed_password = bcrypt_context.hash(password)

csv_file = "cleaned-data/Users.csv"

with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "username", "password", "role"])  # CSV header
    writer.writerow([admin_id, username, hashed_password, role])
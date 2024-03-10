from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Create a connection string
db_url = f"postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
# Create the SQLAlchemy engine
engine = create_engine(db_url)

# Test the connection
try:
    connection = engine.connect()
    print("Connected to the database!")
    connection.close()
except Exception as e:
    print(f"Error: {e}")




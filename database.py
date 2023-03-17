import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load key-value pairs from .env file
load_dotenv()

# The connection string for database from environment variable
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Initialize sqlalchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Create a local session for the connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize declarative base for sqlalchemy models
Base = declarative_base()
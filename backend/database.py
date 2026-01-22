from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# For local development, we default to SQLite for zero-config setup.
# To use PostgreSQL, set DATABASE_URL in .env
# Example: postgresql://user:password@localhost/jedi_bot_db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./jedi_bot.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

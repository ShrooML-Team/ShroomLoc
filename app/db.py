from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

DATABASE_URL = "sqlite:///./shroomloc.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        from app.auth import create_user
        if not db.query(User).filter(User.username == "admin").first():
            create_user("admin", "password123")
            print("Admin user created")
        else:
            print("Admin user already exists")
    finally:
        db.close()


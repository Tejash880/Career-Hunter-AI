"""
Database session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    pool_pre_ping=True,
    echo=False
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create scoped session for thread safety
db_session = scoped_session(SessionLocal)

# Base class for models
Base = declarative_base()
Base.query = db_session.query_property()


def get_db():
    """
    Dependency to get DB session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import event
from app.core.config import get_settings


settings = get_settings() 
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # True para debug, False en prod
)

SQLModel.metadata.create_all(engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    with Session(engine) as session:
        yield session
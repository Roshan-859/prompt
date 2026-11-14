from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.core.config import settings

# Engine configuration with Supabase / Transaction pooler compatibility
engine_kwargs = {
    "pool_pre_ping": True,
}

# If using Supabase transaction pooler (port 6543), disable prepared statement caches
if ":6543" in settings.DATABASE_URL:
    engine_kwargs["connect_args"] = {
        "prepare_threshold": None
    }
else:
    engine_kwargs["pool_size"] = 10
    engine_kwargs["max_overflow"] = 20

engine = create_engine(settings.DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

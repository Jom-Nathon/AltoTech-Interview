from sqlmodel import Session, select, create_engine
from ..config import settings

Postgres_URL = settings.POSTGRES_URL
Supabase_URL = settings.SUPABASE_URL

postgres_engine = create_engine(Postgres_URL)
supabase_engine = create_engine(Supabase_URL)

def get_postgres_session():
    try:
        with Session(postgres_engine) as session:
            yield session
    finally:
        session.close()

def get_supabase_session():
    try:
        with Session(supabase_engine) as session:
            yield session
    finally:
        session.close()

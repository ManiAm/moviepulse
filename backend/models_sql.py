from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://tmdb_user:tmdb_pass@localhost:5432/tmdb_db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class MovieDetail(Base):
    __tablename__ = "movie_detail"

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, unique=True, nullable=False)
    data = Column(JSON, nullable=False)

class CreditDetail(Base):
    __tablename__ = "credit_detail"

    id = Column(Integer, primary_key=True)
    credit_id = Column(String, unique=True, nullable=False)
    data = Column(JSON, nullable=False)


def init_db():
    Base.metadata.create_all(engine)

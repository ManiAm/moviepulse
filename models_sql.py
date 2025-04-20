
# Author: Mani Amoozadeh
# Email: mani.amoozadeh2@gmail.com
# Description: model for interacting with Postgresql

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy import UniqueConstraint

DATABASE_URL = "postgresql://tmdb_user:tmdb_pass@localhost:5432/tmdb_db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    tmdb_id = Column(Integer, nullable=False)   # Movie or TV show ID from TMDB
    media_type = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("username", "tmdb_id", "media_type", name="_username_media_uc"),
    )

    def __repr__(self):
        return f"<Favorite username={self.username} tmdb_id={self.tmdb_id} media_type={self.media_type}>"


def init_db():
    Base.metadata.create_all(engine)

import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Video(Base):
    __tablename__ = 'videos'
    video_id = Column(Integer, primary_key=True, autoincrement=True)
    video_name = Column(String(255), nullable=False)
    video_path = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

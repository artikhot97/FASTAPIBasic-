from sqlalchemy import Column,Integer, String,Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import timezone, datetime


class User(Base):
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True,nullable=False)
    email = Column(String,nullable=False,unique=True,index=True)
    hashed_password = Column(String,nullable=False)
    is_active = Column(Boolean(),default=True)
    is_superuser = Column(Boolean(),default=False)
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    # # job_id = Column(Integer, ForeignKey('job.id'))
    # jobs = relationship('Job',back_populates="owner")
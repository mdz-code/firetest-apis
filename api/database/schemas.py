import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.orm import relationship

from api.config.postgres import Base


class User(Base):

    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    complete_name = Column(String)



class Premium(Base):

    __tablename__ = "premium"

    id = Column(UUID, primary_key=True, index=True)
    user_id = relationship("User", back_populates="id")
    is_premium = Column(Boolean, default=False)
    subscription_date = Column(DateTime, default=datetime.datetime.utcnow)
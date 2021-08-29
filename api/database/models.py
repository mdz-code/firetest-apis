import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from api.config.postgres import Base


class User(Base):

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    complete_name = Column(String)



class Premium(Base):

    __tablename__ = "premium"

    id = Column(UUID, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, unique=True)
    is_premium = Column(Boolean, default=False)
    subscription_date = Column(DateTime, default=datetime.datetime.utcnow)
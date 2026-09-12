from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..utils.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column( Integer , primary_key=True , index=True)
    email = Column( String, unique=True , index=True, nullable=False)
    name = Column(String)
    password = Column(String)

    bookings = relationship("Bookings" , back_populates="user")
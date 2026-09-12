from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..utils.db import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column( String , primary_key=True , index=True )
    name = Column( String , unique=True , nullable=False , index=True)
    capacity = Column( Integer , nullable=False )

    bookings = relationship("Bookings" , back_populates="room")
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from ..utils.db import Base

class Bookings(Base):
    __tablename__ = "bookings"

    id = Column( String , primary_key=True )
    user_id = Column( String , ForeignKey("users.id"))
    room_id = Column( String , ForeignKey("rooms.id"))
    start_time = Column( DateTime , nullable=False )
    end_time = Column( DateTime , nullable=False )
    status = Column( String , default="confirmed" , nullable=False )
    created_at = Column( DateTime , nullable=False)

    user = relationship( "User" , back_populates="bookings")
    room = relationship( "Room" , back_populates="bookings")
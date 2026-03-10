from config.database.index import Base
from sqlalchemy import Column,Integer,String,DateTime
from datetime import datetime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship


class Post(Base):
    __tablename__ = "posts"

    id:Mapped[int] = mapped_column( primary_key=True,unique=True)
    title:Mapped[str]=mapped_column(String(500))
    content:Mapped[str] = mapped_column(String(500))
    like:Mapped[int] = mapped_column(Integer)
    dislike:Mapped[int]= mapped_column(Integer)
    image:Mapped[int]=mapped_column(String(255))
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"),nullable=False)  

    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="posts")  
    comments = relationship("Comment", back_populates="post")  

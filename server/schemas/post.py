from config.database.index import Base
from sqlalchemy import Column,Integer,String,DateTime
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    content = Column(String(500))
    like = Column(Integer)
    dislike = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)  

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="posts")  
    comments = relationship("Comment", back_populates="post")  

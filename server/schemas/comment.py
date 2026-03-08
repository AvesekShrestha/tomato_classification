
from sqlalchemy import Column,Integer,String,DateTime
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from config.database.index import Base


class Comment(Base):
    __tablename__="comment"
    id=Column(Integer,primary_key=True,index=True)
    content=Column(String(500))
    user_id=Column(ForeignKey("User.id"),nullable=False)
    post_id=Column(ForeignKey("Post.id"),nullable=False)
    
    created_at=Column(DateTime,default=datetime.now)
    updated_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)

    user=relationship("User",back_populates="comments")
    post=relationship("Post",back_populates="comments")
   


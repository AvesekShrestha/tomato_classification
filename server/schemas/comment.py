from sqlalchemy import Column,Integer,String,DateTime
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship,mapped_column,Mapped
from config.database.index import Base


class Comment(Base):

    __tablename__ = "comment"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    content:Mapped[str] = mapped_column(String(500))
    user_id:Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    post_id :Mapped[str]= mapped_column(ForeignKey("posts.id"), nullable=False)
    
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

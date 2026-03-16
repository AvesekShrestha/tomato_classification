from config.database.index import Base
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(String(500))
    image: Mapped[str] = mapped_column(String(100), nullable=True)
    like: Mapped[int] = mapped_column(Integer, default=0)
    dislike: Mapped[int] = mapped_column(Integer, default=0)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="posts"
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post"
    )

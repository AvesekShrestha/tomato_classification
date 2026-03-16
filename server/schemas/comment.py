from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from config.database.index import Base

class Comment(Base):

    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(String(500))
    like : Mapped[int] = mapped_column(Integer, default=0)
    dislike : Mapped[int] = mapped_column(Integer, default=0)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"),
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
        back_populates="comments"
    )
    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments"
    )

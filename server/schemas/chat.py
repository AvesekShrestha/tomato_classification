from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from config.database.index import Base


class Chat(Base) :

    __tablename__ = "chats"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    message : Mapped[str] = mapped_column(String(200))
    sender_id : Mapped[int] = mapped_column(Integer, nullable=False)
    receiver_id : Mapped[int] = mapped_column(Integer, nullable=False)
    is_read : Mapped[bool] = mapped_column(Boolean, default=False)
    messaged_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now()) 

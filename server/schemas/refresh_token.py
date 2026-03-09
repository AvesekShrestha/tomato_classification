from config.database.index import Base
from sqlalchemy import DateTime, Integer, String, ForeignKey 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class RefreshToken(Base) : 

    __tablename__ = "refresh_tokens"

    id : Mapped[int] = mapped_column(primary_key=True, unique=True)
    token : Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at : Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user = relationship("User", back_populates="refresh_tokens")


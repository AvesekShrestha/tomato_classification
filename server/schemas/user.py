from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Boolean, DateTime, String
from config.database.index import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum
from routes.v1.user.dto.user_role import UserRole
from sqlalchemy.orm import relationship

class UserStatus(str, Enum) :
    PENDING = "pending",
    ACTIVE = "active",
    REJECTED = "rejected"


class User(Base) : 

    __tablename__ = "users" 

    id : Mapped[int] = mapped_column(primary_key=True, unique=True)
    username : Mapped[str] = mapped_column(String(90))
    email : Mapped[str] = mapped_column(String(90), unique=True)
    password : Mapped[str] = mapped_column(String(200))
    role : Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.FARMER) 
    is_verified : Mapped[bool] = mapped_column(Boolean, default=False)
    otp : Mapped[Optional[str]] = mapped_column(String(6), default=None)
    otp_expires_at : Mapped[Optional[datetime]] = mapped_column(DateTime)
    status : Mapped[UserStatus] = mapped_column(SQLEnum(UserStatus), default=UserStatus.ACTIVE)


    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user")


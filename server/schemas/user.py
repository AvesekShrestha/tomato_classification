from sqlalchemy import String
from config.database.index import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum
from routes.v1.user.dto.user_role import UserRole
from sqlalchemy.orm import relationship
from schemas.post import Post
from schemas.comment import Comment

class User(Base) : 

    __tablename__ = "users" 

    id : Mapped[int] = mapped_column(primary_key=True, unique=True)
    username : Mapped[str] = mapped_column(String(90))
    email : Mapped[str] = mapped_column(String(90), unique=True)
    password : Mapped[str] = mapped_column(String(200))
    role : Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.USER) 


    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user")


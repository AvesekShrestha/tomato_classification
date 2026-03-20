from enum import Enum
from sqlalchemy import Boolean, ForeignKey, Integer, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from config.database.index import Base

class TargetType(str, Enum):
    POST = "post"
    COMMENT = "comment"


class Reaction(Base):

    __tablename__ = "reactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_like: Mapped[bool] = mapped_column(Boolean, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    target_id: Mapped[int] = mapped_column(Integer, nullable=False)
    target_type: Mapped[TargetType] = mapped_column(
        SQLEnum(TargetType), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("user_id", "target_id", "target_type", name="unique_user_reaction"),
    )

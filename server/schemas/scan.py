from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from config.database.index import Base


class Scan(Base):
    __tablename__ = "scan_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    image_url: Mapped[str] = mapped_column(String(255), nullable=False)

    predicted_class: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    cause: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    prescriptions: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    scanned_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

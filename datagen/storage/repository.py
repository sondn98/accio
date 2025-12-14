from sqlalchemy import BLOB, BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Storage(DeclarativeBase):
    __tablename__ = "storage"

    id: Mapped[int] = (mapped_column(BigInteger, primary_key=True),)
    dataset: Mapped[str] = (mapped_column(String, nullable=False, index=True),)
    data: Mapped[bytes] = (mapped_column(BLOB, nullable=False),)
    order: Mapped[int] = mapped_column(BigInteger, nullable=True)

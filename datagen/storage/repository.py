from sqlalchemy import BLOB, Integer, BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class StorageBase(DeclarativeBase):
    pass


class Storage(StorageBase):
    __tablename__ = "storage"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    dataset: Mapped[str] = mapped_column(String, nullable=False, index=True)
    data: Mapped[bytes] = mapped_column(BLOB, nullable=False)
    order: Mapped[int] = mapped_column(BigInteger, nullable=True)

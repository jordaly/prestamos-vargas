from pathlib import Path
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
    sessionmaker,
    Mapped,
    mapped_column,
)

from sqlalchemy import (
    create_engine,
    ForeignKey,
    VARCHAR,
    FLOAT,
    func,
)


class Base(DeclarativeBase):
    # __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(VARCHAR(60), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(60), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(VARCHAR(60), unique=True)
    first_name: Mapped[Optional[str]] = mapped_column(VARCHAR(60))
    last_name: Mapped[Optional[str]] = mapped_column(VARCHAR(60))
    image: Mapped[Optional[str]] = mapped_column(VARCHAR(60))

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email}, first_name={self.first_name}, last_name={self.last_name})>"


class Client(Base):
    __tablename__ = "clients"
    name: Mapped[str] = mapped_column(VARCHAR(60), nullable=False)

    loans: Mapped[List["Loan"]] = relationship(back_populates="client")
    payments: Mapped[List["Payment"]] = relationship(back_populates="client")

    def __repr__(self):
        return f"<Client(name={self.name})>"


class Loan(Base):
    __tablename__ = "loans"

    cliend_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))

    amount: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.current_timestamp(), default=None
    )
    updated_at: Mapped[datetime] = mapped_column(
        insert_default=func.current_timestamp(), default=None
    )

    client: Mapped["Client"] = relationship(back_populates="loans")
    payments: Mapped[List["Payment"]] = relationship(back_populates="loan")

    def __repr__(self):
        return f"<Loan(amount={self.amount}, created_at={self.created_at})>"


class Payment(Base):
    __tablename__ = "payments"

    loan_id: Mapped[int] = mapped_column(ForeignKey("loans.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))

    amount: Mapped[float] = mapped_column(FLOAT, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, insert_default=func.current_timestamp(), default=None
    )

    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, insert_default=func.current_timestamp(), default=None
    )

    loan: Mapped["Loan"] = relationship(back_populates="payments")

    client: Mapped["Client"] = relationship(back_populates="payments")

    def __repr__(self):
        return f"<Payment(amount={self.amount}, created_at={self.created_at})>"


current_path = Path(__file__).resolve().parent.parent

DB_URI = f"sqlite:///{current_path / 'database.db'}"

engine = create_engine(DB_URI, echo=True)


# print(f"The current path is: \n{current_path.parent.parent}")


def create_database():
    Base.metadata.create_all(bind=engine)


Session = sessionmaker(bind=engine)

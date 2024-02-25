from pathlib import Path
from typing import List, Optional, Type, TypeVar
from datetime import datetime
from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
    sessionmaker,
    Mapped,
    mapped_column,
    Session,
)

from sqlalchemy import (
    create_engine,
    ForeignKey,
    VARCHAR,
    FLOAT,
    func,
    select,
)

CURRENT_PATH = Path(__file__).resolve().parent.parent

DB_URI = f"sqlite:///{CURRENT_PATH / 'database.db'}"

engine = create_engine(DB_URI, echo=True)


class Base(DeclarativeBase):
    session = sessionmaker(bind=engine)
    # __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)

    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.current_timestamp(), default=None
    )

    updated_at: Mapped[datetime] = mapped_column(
        insert_default=func.current_timestamp(), default=None
    )

    instance_of_current_class = TypeVar("instance_of_current_class", bound=__name__)

    def save(self) -> None:
        """saves record"""
        with self.session.begin() as session:
            session.add(self)
            session.commit()

    def delete(self) -> None:
        """deletes record"""
        with self.session.begin() as session:
            session.delete(self)
            session.commit()

    def update(self, **kwargs) -> None:
        """update record"""
        with self.session.begin() as session:
            for key, value in kwargs.items():
                setattr(self, key, value)
            session.add(self)
            session.commit()

    @classmethod
    def get(
        cls: Type[instance_of_current_class], **kwargs
    ) -> instance_of_current_class:
        """get a single record, cant be
        called from instances of the class"""
        with cls.session() as session:
            return session.scalars(select(cls).filter_by(**kwargs).limit(1)).one()

    @classmethod
    def all(cls: Type[instance_of_current_class]) -> List[instance_of_current_class]:
        """get all instances, cant be
        called from instances of the class"""
        with cls.session() as session:
            return session.scalars(select(cls)).all()

    @classmethod
    def filter(
        cls: Type[instance_of_current_class], **kwargs
    ) -> List[instance_of_current_class]:
        """get all matching instances, cant
        be called from instances of the class"""
        with cls.session() as session:
            if "limit" in kwargs:
                limit = int(kwargs.pop("limit"))
                result = session.scalars(
                    select(cls).filter_by(**kwargs).limit(limit)
                ).all()
                return result

            result = session.scalars(select(cls).filter_by(**kwargs).limit(1))
            return result


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

    client: Mapped["Client"] = relationship(back_populates="loans")
    payments: Mapped[List["Payment"]] = relationship(back_populates="loan")

    def __repr__(self):
        return f"<Loan(amount={self.amount}, created_at={self.created_at})>"


class Payment(Base):
    __tablename__ = "payments"

    loan_id: Mapped[int] = mapped_column(ForeignKey("loans.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))

    amount: Mapped[float] = mapped_column(FLOAT, nullable=False)

    loan: Mapped["Loan"] = relationship(back_populates="payments")

    client: Mapped["Client"] = relationship(back_populates="payments")

    def __repr__(self):
        return f"<Payment(amount={self.amount}, created_at={self.created_at})>"


# print(f"The current path is: \n{current_path.parent.parent}")


def create_database():
    Base.metadata.create_all(bind=engine)

from typing import Optional

from sqlmodel import SQLModel, Field


class Bank(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)


class Credit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bank_id: int = Field(foreign_key=Bank.id)
    user_id: int = Field(foreign_key=User.id)
    summary: float = Field(default=0.0)


class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key=User.id)
    type: str = Field(nullable=False)
    text: str = Field(nullable=False)
    photos: str = Field(nullable=False)

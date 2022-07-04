from typing import Any

from sqlmodel import select, SQLModel, Session


def get_or_create(
    session: Session, model: SQLModel.__class__, params: list[tuple[str, Any]]
):
    conditions = [getattr(model, param) == value for param, value in params]
    stmt = select(model).where(*conditions)
    obj = session.exec(stmt).one_or_none()
    if not obj:
        obj = model(**{param: value for param, value in params})
        session.add(obj)
        session.commit()
        session.refresh(obj)
    return obj


def get_all(
    session: Session, model: SQLModel.__class__, params: list[tuple[str, Any]]
):
    conditions = [getattr(model, param) == value for param, value in params]
    stmt = select(model).where(*conditions)
    return session.exec(stmt).all()

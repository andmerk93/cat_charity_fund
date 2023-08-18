from sqlalchemy import Column, String, Text

from app.core.db import Base

from .abstract_parent import AbstractParent


class CharityProject(AbstractParent, Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return self.name

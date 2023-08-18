from sqlalchemy import Column, Integer, Text, ForeignKey

from app.core.db import Base

from .abstract_parent import AbstractParent


class Donation(AbstractParent, Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)

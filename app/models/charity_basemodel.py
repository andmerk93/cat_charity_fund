from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class CharityBaseModel(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount >= 0'),
        CheckConstraint('invested_amount <= full_amount'),
    )

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, index=True, default=datetime.utcnow)
    close_date = Column(DateTime, default=None)

    def __repr__(self):
        return (
            f'full_amount={self.full_amount},'
            f'invested_amount={self.invested_amount},'
            f'fully_invested={self.fully_invested},'
            f'create_date={self.create_date},'
            f'close_date={self.close_date}'
        )

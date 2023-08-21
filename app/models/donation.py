from sqlalchemy import Column, Integer, Text, ForeignKey

from .charity_basemodel import CharityBaseModel


class Donation(CharityBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)

    def __repr__(self):
        return super(
            f'user_id={self.user_id},'
            f'comment={self.comment}'
        ).__repr__()

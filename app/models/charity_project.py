from sqlalchemy import Column, String, Text

from .charity_basemodel import CharityBaseModel


class CharityProject(CharityBaseModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'{super().__repr__()},'
            f'name={self.name},'
            f'description={self.description}'
        )

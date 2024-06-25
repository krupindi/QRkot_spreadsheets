from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import AbstractModel


class Donation(AbstractModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

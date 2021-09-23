from sqlalchemy import Column, Integer, String

from lib.schedule.db import Base


class YandexUser(Base):
    __tablename__ = 'yandex_users'
    id = Column(String(512), primary_key=True)
    name = Column(String(512))
    educational_group_id = Column(Integer, nullable=False)
    subgroup = Column(Integer, default=0)

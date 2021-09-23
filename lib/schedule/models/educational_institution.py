from sqlalchemy import Column, Integer, String

from lib.schedule.db import Base


class EducationalInstitution(Base):
    __tablename__ = 'educational_institutions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String(64), unique=True, nullable=False)
    name = Column(String(512), unique=True, nullable=False)
    type_id = Column(Integer, nullable=False)

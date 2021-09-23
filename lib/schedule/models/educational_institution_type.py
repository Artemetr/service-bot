from sqlalchemy import Column, Integer, String

from lib.schedule.db import Base


class EducationalInstitutionType(Base):
    __tablename__ = 'educational_institution_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True)

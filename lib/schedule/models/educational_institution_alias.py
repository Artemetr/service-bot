from sqlalchemy import Column, Integer, String

from lib.schedule.db import Base


class EducationalInstitutionAlias(Base):
    __tablename__ = 'educational_institution_aliases'
    educational_institution_id = Column(Integer, nullable=False)
    alias = Column(String(512), primary_key=True)

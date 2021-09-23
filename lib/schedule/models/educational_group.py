from sqlalchemy import Column, Integer, String, JSON, Text

from lib.schedule.db import Base


class EducationalGroup(Base):
    __tablename__ = 'educational_groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    educational_institution_id = Column(Integer, nullable=False)
    name = Column(String(512), unique=True)
    schedule = Column(JSON, nullable=False, default={})
    url = Column(Text, nullable=False)

    @classmethod
    def get_with_id(cls, id: int):
        from lib.schedule.db import Session

        with Session() as s:
            group: cls or None = s.query(cls).filter(cls.id == id).one_or_none()

        return group


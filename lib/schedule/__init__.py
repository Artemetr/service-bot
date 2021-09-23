from lib.schedule.db import Session, engine, Base
import lib.schedule.models as models

Base.metadata.create_all(bind=engine)

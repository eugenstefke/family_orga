from data.database import Base, engine
import models.models

Base.metadata.create_all(engine)
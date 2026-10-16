"""The file is used to resolve errors in tables """

from data.database import Base, engine
import models.models

Base.metadata.create_all(engine)
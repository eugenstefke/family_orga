from database import Base, engine
import models # wichtig: die Models müssen importiert sein, damit Base sie kennt

Base.metadata.create_all(engine)
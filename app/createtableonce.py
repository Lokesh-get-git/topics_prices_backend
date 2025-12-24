from app.db import engine, Base
from app.models import *

Base.metadata.create_all(bind=engine)
print(' Tables created!')
print('Manually create experience ranges')
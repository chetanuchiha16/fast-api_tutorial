from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

print(Base.metadata)
print(DeclarativeBase.metadata)
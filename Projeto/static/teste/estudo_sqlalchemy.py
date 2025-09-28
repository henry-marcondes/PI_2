
import sys
print(sys.executable)

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import DeclarativeBase
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Integer

class Base(DeclarativeBase):
    pass


class User(Base):
  __tablename__ = 'User'
  idUser: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(String(16))
  email: Mapped[str] = mapped_column(String(255))
  password: Mapped[str] = mapped_column(String(32))
  pessoa_id: Mapped[int] = mapped_column(Integer)
  pessoa: Mapped[List["Pessoa"]] = relationship(back_populates="User")
     

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Language(Base):
    __tablename__ = "languages"

    code = Column(String(2), primary_key=True)
    name = Column(String(50), nullable=False)

    users = relationship("User", back_populates="language")

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    sheets_per_day = Column(Integer, nullable=False)
    password = Column(String(50), nullable=False)

    users = relationship("User", back_populates="group")

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    language_code = Column(String(2), ForeignKey("languages.code"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    pages_left = Column(Integer, nullable=False)

    language = relationship("Language", back_populates="users")
    group = relationship("Group", back_populates="users")
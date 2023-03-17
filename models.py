from sqlalchemy import Boolean, Integer, String, Column, ForeignKey, text
from sqlalchemy.orm import relationship

try:
    from .database import Base
except:
    from database import Base

# Define models for tables in database
class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    status = Column(String(50), nullable=False,)

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    designation = Column(String(50), nullable=False)

class Interview(Base):
    __tablename__="interviews"

    id = Column(Integer, primary_key=True, index=True)
    round = Column(Integer, nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    candidates = relationship("Candidate")
    employees = relationship("Employee")


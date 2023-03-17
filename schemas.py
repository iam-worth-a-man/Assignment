from pydantic import BaseModel

# Define pydantic models for data validation
class CandidateBase(BaseModel):
    name: str
    email: str
    status: str

    class Config:
        orm_mode = True


class Candidate(CandidateBase):
    id: int

    class Config:
        orm_mode = True


class EmployeeBase(BaseModel):
    name: str
    email: str
    designation: str

    class Config:
        orm_mode = True


class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True


class InterviewBase(BaseModel):
    round: int
    candidate_id: int
    employee_id: int

    class Config:
        orm_mode = True


class Interview(InterviewBase):
    id: int

    class Config:
        orm_mode = True
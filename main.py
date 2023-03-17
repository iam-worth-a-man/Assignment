from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, PendingRollbackError

try:
    from . import crud, models, schemas
    from .database import SessionLocal, engine
except:
    import crud, models, schemas
    from database import SessionLocal, engine

# Bind the engine to create all tables
models.Base.metadata.create_all(bind=engine)

# Initalize the fastapi app
app = FastAPI()


# Create dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/candidate/{candidate_id}", response_model=schemas.Candidate)
def read_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """
    Fetch the candidate using :
    - **id**: Id of the candidate to be fetched

    \f
    : param candidate_id: candidate's id
    """

    # Fetch the candidate using id
    db_candidate = crud.get_candidate(db, candidate_id=candidate_id)

    # Verify if the candidate exists
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Return the fetched candidate
    return db_candidate


@app.get("/candidates/", response_model=list[schemas.Candidate])
def read_candidates(name: str = None, email: str=None, status: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Fetch the candidate using :
    - **name**: full name of the candidate
    - **email**: personal email of the candidate
    - **status**: current hiring status of the candidate, Ex: "pre-hire", "active", "inactive"

    """

    # Fetch the candidate by applying all the filters
    candidates = crud.get_candidates(db, name, email, status, skip=skip, limit=limit)

    # Verify if the candidates exists
    if not candidates:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Return the list of fetched candidates
    return candidates


@app.post("/candidate/", response_model=schemas.Candidate, status_code=201)
def create_candidate(candidate: schemas.CandidateBase, db: Session = Depends(get_db)):
    """
    Create a candidate with following information:

    - **name**: full name of the candidate
    - **email**: personal email of the candidate
    - **status**: current hiring status of the candidate, Ex: "pre-hire", "active", "inactive"

    \f
    :param candidate: Candidate model input
    """

    # Sanity checks on post body
    if not candidate.name.strip():
        raise HTTPException(status_code=400, detail="Please enter the candidate name")
    if not candidate.email.strip():
        raise HTTPException(status_code=400, detail="Please enter the candidate email")
    if not candidate.status.strip():
        raise HTTPException(status_code=400, detail="Please enter the candidate status")

    # Verify existence of given email in database
    db_candidate = crud.get_candidate_by_email(db, email=candidate.email)
    if db_candidate:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create and return the candidate
    return crud.create_candidate(db=db, candidate=candidate)

@app.delete("/candidate/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """
    Delete the candidate using :
    - **candidate_id**: Id of the candidate to be deleted

    \f
    : param candidate_id: candidate's id
    """

    # Verify if the candidate exists
    db_candidate = crud.get_candidate(db, candidate_id=candidate_id)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Verify if the candidate has any interview scheduled, else delete the candidate
    interviews = crud.get_interviews(db, candidate_id=candidate_id)
    if interviews:
        raise HTTPException(status_code=400, detail="Candidate can not be deleted as its interview is scheduled")
    else:
        res = crud.destroy_candidate(db, id=candidate_id)

    # Return the response as per the integer status
    if res:
        return {"detail":"Candidate Deleted Successfully"}
    return {"detail":"Candidate Deletion Unsuccessful"}


@app.delete("/candidate/")
def delete_candidate_by_email(email: str, db:Session = Depends(get_db)):
    """
    Delete the candidate using :
    - **email**: Email id of the candidate to be deleted

    \f
    : param email: candidate's email id
    """

    # Verify if the candidate exists
    db_candidate = crud.get_candidate_by_email(db, email)
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Verify if the candidate has any interview scheduled, else delete the candidate
    interviews = crud.get_interviews(db, candidate_id=db_candidate.id)
    if interviews:
        raise HTTPException(status_code=400, detail="Candidate can not be deleted as its interview is scheduled")
    else:
        res = crud.destroy_candidate_by_email(db, email=email)

    # Return the response as per the integer status
    if res:
        return {"detail":"Candidate Deleted Successfully"}
    return {"detail":"Candidate Deletion Unsuccessful"}


@app.put("/candidate/{candidate_id}")
def update_candidate(candidate_id: int, new_candidate: schemas.CandidateBase, db: Session = Depends(get_db)):
    """
    Update the candidate using:
    - **id**: Id of the candidate to be updated

    \f
    : param candidate_id: candidate's id
    """

    # Verify if the candidate exists
    old_candidate = read_candidate(candidate_id, db)
    if not old_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")


    # Sanity checks on post body
    if not new_candidate.name.strip():
        raise HTTPException(status_code=400, detail="Please enter the candidate name")
    if not new_candidate.email.strip():
        raise HTTPException(status_code=400, detail="Please enter the candidate email")
    if not new_candidate.status.strip():
        raise HTTPException(status_code=400, detail="Please enter the candidate status")

    # verify if the email of new candidate already exists in db
    candidate_email = crud.get_candidate_by_email(db, new_candidate.email)
    if candidate_email and candidate_email.id != candidate_id:
        raise HTTPException(status_code=400, detail="Candidate with the provided email already exists")

    # Append candidate id to CandidateBase schema to make it compatible as per Candidate schema
    temp_record = new_candidate.dict()
    temp_record["id"] = candidate_id
    new_record = models.Candidate(**temp_record)

    # Update the candidate and return details
    crud.put_candidate(db, new_record)
    return {"detail":"Candidate Updated Successfully"}

# ++++++++++++++++++++++++++++++++============

@app.get("/employee/{employee_id}", response_model=schemas.Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    """
    Fetch the employee using :
    - **id**: Id of the employee to be fetched

    \f
    : param employee_id: employee's id
    """
    # Fetch and verify if the employee exists
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Return the fetched employee
    return db_employee



@app.get("/employees/", response_model=list[schemas.Employee])
def read_employees(name: str = None, email: str=None, designation: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Fetch the employee using :

    - **name**: full name of the employee
    - **email**: personal email of the employee
    - **designation**: current hiring designation of the employee, Ex: "CEO", "Developer", "Designer"

    """

    # Fetch the employees by applying all the filters
    employees = crud.get_employees(db, name, email, designation, skip=skip, limit=limit)

    # Verify if any employee exists
    if not employees:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Return list of fetched employees
    return employees


@app.post("/employee/", response_model=schemas.Employee, status_code=201)
def create_employee(employee: schemas.EmployeeBase, db: Session = Depends(get_db)):
    """
    Create a candidate with following information:

    - **name**: full name of the employee
    - **email**: personal email of the employee
    - **designation**: current hiring designation of the employee, Ex: "CEO", "Developer", "Designer"

    \f
    :param employee: Employee model input
    """

    # Sanity checks on post body
    if not employee.name.strip():
        raise HTTPException(status_code=400, detail="Please enter the employee name")
    if not employee.email.strip():
        raise HTTPException(status_code=400, detail="Please enter the employee email")
    if not employee.designation.strip():
        raise HTTPException(status_code=400, detail="Please enter the employee designation")

    # Verify existence of given email in database
    db_employee = crud.get_employee_by_email(db, email=employee.email)
    if db_employee:
        raise HTTPException(status_code=400, detail="Employee with the provided email already exists")
    
    # Create and return the employee
    return crud.create_employee(db=db, employee=employee)

@app.delete("/employee/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """
    Delete the employee using :
    - **employee_id**: Id of the employee to be deleted

    \f
    : param employee_id: employee's id
    """

    # Verify if the candidate exists
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    

    # Verify if the employee has any interview scheduled, else delete the employee
    interviews = crud.get_interviews(db, employee_id=employee_id)
    if interviews:
        raise HTTPException(status_code=400, detail="Employee can not be deleted as its an interviewer")
    else:
        res = crud.destroy_employee(db, id=employee_id)
    
    # Return the response as per the integer status
    if res:
        return {"detail":"Employee Deleted Successfully"}
    return {"detail":"Employee Deletion Unsuccessful"}


@app.delete("/employee/")
def delete_employee_by_email(email: str, db:Session = Depends(get_db)):
    """
    Delete the employee using :
    - **email**: Email d of the employee to be deleted

    \f
    : param email: employee's email id
    """

    # Verify if the candidate exists by email
    db_employee = crud.get_employee_by_email(db, email)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Verify if the employee has any interview scheduled, else delete the employee
    interviews = crud.get_interviews(db, employee_id=db_employee.id)
    if interviews:
        raise HTTPException(status_code=400, detail="Employee can not be deleted as its an interviewer")
    else:
        res = crud.destroy_employee_by_email(db, email=email)

    # Return the response as per the integer status
    if res:
        return {"detail":"Employee Deleted Successfully"}
    return {"detail":"Employee Deletion Unsuccessful"}


@app.put("/employee/{employee_id}")
def update_employee(employee_id: int, new_employee: schemas.EmployeeBase, db: Session = Depends(get_db)):
    """
    Update the employee using:
    - **employee_id**: Id of the employee to be updated

    \f
    : param employee_id: employee's id
    """

    # Verify if the employee exists
    old_employee = read_employee(employee_id, db)
    if not old_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Sanity checks on post body
    if not new_employee.name.strip():
        raise HTTPException(status_code=400, detail="Please enter the employee name")
    if not new_employee.email.strip():
        raise HTTPException(status_code=400, detail="Please enter the employee email")
    if not new_employee.designation.strip():
        raise HTTPException(status_code=400, detail="Please enter the employee designation")

    # verify if the email of new employee already exists in db
    employee_email  = crud.get_employee_by_email(db, new_employee.email)
    if employee_email and employee_email.id != employee_id:
        raise HTTPException(status_code=400, detail="Employee with the provided email already exists")
    
    # Append employee id to EmployeeBase schema to make it compatible as per Employee schema
    temp_record = new_employee.dict()
    temp_record["id"] = employee_id
    new_record = models.Employee(**temp_record)

    # Update the employee and return details
    crud.put_employee(db, new_record)
    return {"detail":"Employee Updated Successfully"}

# +++++++++++++++++++++++++

@app.get("/interview/{interview_id}", response_model=schemas.Interview)
def read_interview(interview_id: int, db: Session = Depends(get_db)):
    """
    Fetch the interview using :
    - **interview_id**: Id of the interview to be fetched

    \f
    : param interview_id: interview id
    """

    # Verify if the interview exists
    db_interview = crud.get_interview(db, interview_id=interview_id)
    if db_interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    # Return the fetched interview
    return db_interview


@app.get("/interviews/", response_model=list[schemas.Interview])
def read_interviews(round: int = None, candidate_id: int=None, employee_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Fetch interviews with following information:

    - **round**: round number of the interview
    - **candidate_id**: Id of the candidate to be interviewed
    - **employee_id**: Id of the employee interviewing

    """

    # Fetch the interviews by applying all the filters
    interviews = crud.get_interviews(db, round, candidate_id, employee_id, skip=skip, limit=limit)

    # Verify if the interview exists
    if not interviews:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    # Return the list of fetched interviews
    return interviews


@app.post("/interview/", response_model=schemas.Interview, status_code=201)
def create_interview(interview: schemas.InterviewBase, db: Session = Depends(get_db)):
    """
    Create an interview with following information:

    - **round**: round number of the interview
    - **candidate_id**: Id of the candidate to be interviewed
    - **employee_id**: Id of the employee interviewing

    \f
    :param interview: Interview model input
    """

    # Sanity checks on post body
    if not interview.round:
        raise HTTPException(status_code=400, detail="Please enter non-zero round")
    if not interview.candidate_id:
        raise HTTPException(status_code=400, detail="Please enter the non-zero candidate id")
    if not interview.employee_id:
        raise HTTPException(status_code=400, detail="Please enter the non-zero employee id")

    # Verify existence of given candidate and employee ID's in database
    db_interview = crud.get_interviews(db, candidate_id=interview.candidate_id, employee_id=interview.employee_id)
    if db_interview:
        raise HTTPException(status_code=400, detail="Interview already scheduled")

    # Fetch and verify if any of the provided candidate id or employee id is not registered
    isCandidate = crud.get_candidate(db, interview.candidate_id)
    isEmployee = crud.get_employee(db, interview.employee_id)

    if not isCandidate:
        raise HTTPException(status_code=400, detail="Candidate to be interviewed is not registered")
    elif not isEmployee:
        raise HTTPException(status_code=400, detail="Employee as Interviewer is not available")
    else:
        # Create and return the interview 
        res = crud.create_interview(db=db, interview=interview)
        return res



@app.delete("/interview/{interview_id}")
def delete_interview(interview_id: int, db: Session = Depends(get_db)):
    """
    Delete the interview using :
    - **interview_id**: Id of the interview to be deleted

    \f
    : param interview_id: interview id
    """

    # Verify if the interview exists
    db_interview = crud.get_interview(db, interview_id=interview_id)
    if db_interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    # Delete the interview and return the response as per the integer status
    res = crud.destroy_interview(db, id=interview_id)
    if res:
        return {"detail":"Interview Deleted Successfully"}
    return {"detail":"Interview Deletion Unsuccessful"}


@app.put("/interview/{interview_id}")
def update_interview(interview_id: int, new_interview: schemas.InterviewBase, db: Session = Depends(get_db)):
    """
    Update the interview using:
    - **interview_id**: Id of the interview to be updated

    \f
    : param interview_id: interview id
    """

    # Verify if the interview exists
    old_interview = read_interview(interview_id, db)
    if not old_interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    # Fetch and verify if any of the provided candidate id or employee id is not registered
    isCandidate = crud.get_candidate(db, new_interview.candidate_id)
    isEmployee = crud.get_employee(db, new_interview.employee_id)

    if not isCandidate:
        raise HTTPException(status_code=400, detail="Candidate to be interviewed is not registered")
    elif not isEmployee:
        raise HTTPException(status_code=400, detail="Employee as Interviewer is not available")
    else:
        # Append interview id to InterviewBase schema to make it compatible as per Interview schema
        temp_record = new_interview.dict()
        temp_record["id"] = interview_id
        new_record = models.Interview(**temp_record)

        # Create and return the details
        crud.put_interview(db, new_record)
        return {"detail":"Interview Updated Successfully"}
from sqlalchemy.orm import Session

try:
    from . import models, schemas
except:
    import models, schemas

def get_candidate(db: Session, candidate_id: int):
    """
    Fetch the candidate with given id

    :param db: Existing database session
    :param candidate_id: Id of the candidate to be fetched

    :returns result: Single candidate record
    """

    # Build and Return the query after adding filter
    return db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()

def get_candidate_by_name(db: Session, name: str):
    """
    Fetch the candidate with given name

    :param db: Existing database session
    :param name: Name of the candidate to be fetched

    :returns result: Single candidate record
    """

    # Build and Return the query after adding name filter
    return db.query(models.Candidate).filter(models.Candidate.name == name).first()

def get_candidate_by_email(db: Session, email: str):
    """
    Fetch the candidate with given email id

    :param db: Existing database session
    :param email: Email id of the candidate to be fetched

    :returns result: Single candidate record
    """

    # Build and Return the query after adding email filter
    return db.query(models.Candidate).filter(models.Candidate.email == email).first()

def get_candidate_by_status(db: Session, status: str):
    """
    Fetch the candidate with given status

    :param db: Existing database session
    :param status: Status of the candidate to be fetched

    :returns result: Single candidate record
    """

    # Build and Return the query after adding status filter
    return db.query(models.Candidate).filter(models.Candidate.status == status).first()


def get_candidates(db: Session, name: str = None, email: str=None, status: str = None, skip: int = 0, limit: int = 100):
    """
    Fetch all candidates with given filters

    :param db: Existing database session
    :param name: Name of the candidate to be fetched
    :param email: Email id of the candidate to be fetched
    :param status: Status of the candidate to be fetched
    :param skip: Number of records to skip
    :param limit: Number of records to return after skipping

    :returns results: List of candidate records
    """

    # Build a query for the candidates table
    query = db.query(models.Candidate)

    # Add filters to the query
    if name:
        query = query.filter(models.Candidate.name == name)
    if email:
        query = query.filter(models.Candidate.email == email)
    if status:
        query = query.filter(models.Candidate.status == status)

    # Return list of records after adding offset and limit
    return query.offset(skip).limit(limit).all()


def create_candidate(db: Session, candidate: schemas.CandidateBase):
    """
    Create the candidate with given candidate schema

    :param db: Existing database session
    :param candidate: Schema of the candidate to be created

    :returns result: Single created candidate record
    """

    # Initialize candidate model object
    db_candidate = models.Candidate(name=candidate.name, email=candidate.email, status=candidate.status)
    
    # Add and Commit the record in the table
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)

    # Return created candidate
    return db_candidate

def destroy_candidate(db: Session, id: int):
    """
    Delete the candidate with given candidate id

    :param db: Existing database session
    :param id: Id of the candidate to be deleted

    :returns result: Integer status of deletion
    """

    # Build and Commit the delete query
    res = db.query(models.Candidate).filter(models.Candidate.id == id).delete()
    db.commit()

    # Return the integer status of deletion
    return res

def destroy_candidate_by_email(db: Session, email: str):
    """
    Delete the candidate with given candidate email

    :param db: Existing database session
    :param email: Email of the candidate to be deleted

    :returns result: Integer status of deletion
    """

    # Build and Commit the delete query by email
    res = db.query(models.Candidate).filter(models.Candidate.email==email).delete()
    db.commit()

    # Return the integer status of deletion
    return res

def put_candidate(db: Session, new_candidate: models.Candidate):
    """
    Update the candidate with given candidate schema

    :param db: Existing database session
    :param candidate: Schema of the new candidate

    """

    # Build and Commit the update query by merging the record
    res = db.merge(new_candidate)
    db.commit()
    return res


def get_employee(db: Session, employee_id: int):
    """
    Fetch the employee with given id

    :param db: Existing database session
    :param employee_id: Id of the employee to be fetched

    :returns result: Single employee record
    """

    # Build and Return the query after adding filter
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

def get_employee_by_name(db: Session, name: str):
    """
    Fetch the employee with given name

    :param db: Existing database session
    :param name: Name of the employee to be fetched

    :returns result: Single employee record
    """

    # Build and Return the query after adding name filter
    return db.query(models.Employee).filter(models.Employee.name == name).first()

def get_employee_by_email(db: Session, email: str):
    """
    Fetch the employee with given email id

    :param db: Existing database session
    :param email: Email id of the employee to be fetched

    :returns result: Single employee record
    """

    # Build and Return the query after adding email filter
    return db.query(models.Employee).filter(models.Employee.email == email).first()

def get_employee_by_designation(db: Session, designation: str):
    """
    Fetch the employee with given designation

    :param db: Existing database session
    :param designation: Designation of the employee to be fetched

    :returns result: Single employee record
    """

    # Build and Return the query after adding designation filter
    return db.query(models.Employee).filter(models.Employee.designation == designation).first()

def get_employees(db: Session, name: str = None, email: str=None, designation: str = None, skip: int = 0, limit: int = 100):
    """
    Fetch all employees with given filters

    :param db: Existing database session
    :param name: Name of the employee to be fetched
    :param email: Email id of the employee to be fetched
    :param designation: Designation of the employee to be fetched
    :param skip: Number of records to skip
    :param limit: Number of records to return after skipping

    :returns results: List of employee records 
    """

    # Build a query for the employees table
    query = db.query(models.Employee)

    # Add filters to the query
    if name:
        query = query.filter(models.Employee.name == name)
    if email:
        query = query.filter(models.Employee.email == email)
    if designation:
        query = query.filter(models.Employee.designation == designation)

    # Return list of records after adding offset and limit
    return query.offset(skip).limit(limit).all()


def create_employee(db: Session, employee: schemas.EmployeeBase):
    """
    Create the employee with given employee schema

    :param db: Existing database session
    :param employee: Schema of the employee to be created

    :returns result: Single created employee record
    """

    # Initialize employee model object
    db_employee = models.Employee(name=employee.name, email=employee.email, designation=employee.designation)

    # Add and Commit the record in the table
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    # Return created employee
    return db_employee

def destroy_employee(db: Session, id: int):
    """
    Delete the employee with given employee id

    :param db: Existing database session
    :param id: Id of the employee to be deleted

    :returns result: Integer status of deletion
    """

    # Build and Commit the delete query
    res = db.query(models.Employee).filter(models.Employee.id == id).delete()
    db.commit()

    # Return the integer status of deletion
    return res

def destroy_employee_by_email(db: Session, email: str):
    """
    Delete the employee with given employee email

    :param db: Existing database session
    :param email: Email of the employee to be deleted

    :returns result: Integer status of deletion
    """

    # Build and Commit the delete query by email
    res = db.query(models.Employee).filter(models.Employee.email==email).delete()
    db.commit()

    # Return the integer status of deletion
    return res


def put_employee(db: Session, new_employee: models.Employee):
    """
    Update the employee with given employee schema

    :param db: Existing database session
    :param employee: Schema of the new employee

    """

    # Build and Commit the update query by merging the record
    res = db.merge(new_employee)
    db.commit()
    return res


def get_interview(db: Session, interview_id: int):
    """
    Fetch the interview with given id

    :param db: Existing database session
    :param interview_id: Id of the interview to be fetched

    :returns result: Single interview record
    """

    # Build and Return the query after adding filter
    return db.query(models.Interview).filter(models.Interview.id == interview_id).first()

def get_interview_by_round(db: Session, round: int):
    """
    Fetch the interview with given round

    :param db: Existing database session
    :param round: round of the interview to be fetched

    :returns result: Single interview record
    """

    # Build and Return the query after adding round filter
    return db.query(models.Interview).filter(models.Interview.round == round).first()

def get_interview_by_candidate(db: Session, candidate_id: int):
    """
    Fetch the interview with given candidate_id

    :param db: Existing database session
    :param candidate_id: Candidate Id of the interview to be fetched

    :returns result: Single interview record
    """

    # Build and Return the query after adding candidate_id filter
    return db.query(models.Interview).filter(models.Interview.candidate_id == candidate_id).first()

def get_interview_by_employee(db: Session, employee_id: int):
    """
    Fetch the interview with given employee id

    :param db: Existing database session
    :param employee_id: Employee Id of the interview to be fetched

    :returns result: Single interview record
    """

    # Build and Return the query after adding employee_id filter
    return db.query(models.Interview).filter(models.Interview.employee_id == employee_id).first()

def get_interviews(db: Session, round: str = None, candidate_id: str=None, employee_id: str = None, skip: int = 0, limit: int = 100):
    """
    Fetch all interviews with given filters

    :param db: Existing database session
    :param round: round of the interview to be fetched
    :param candidate_id: Candidate Id of the interview to be fetched
    :param employee_id: Employee Id of the interview to be fetched
    :param skip: Number of records to skip
    :param limit: Number of records to return after skipping

    :returns results: List of interview records 
    """

    # Build a query for the interviews table
    query = db.query(models.Interview)

    # Add filters to the query
    if round:
        query = query.filter(models.Interview.round == round)
    if candidate_id:
        query = query.filter(models.Interview.candidate_id == candidate_id)
    if employee_id:
        query = query.filter(models.Interview.employee_id == employee_id)

    # Return list of records after adding offset and limit
    return query.offset(skip).limit(limit).all()

def create_interview(db: Session, interview: schemas.InterviewBase):
    """
    Create the interview with given interview schema

    :param db: Existing database session
    :param interview: Schema of the interview to be created

    :returns result: Single created interview record
    """

    # Initialize interview model object
    db_interview = models.Interview(round=interview.round, candidate_id = interview.candidate_id, employee_id = interview.employee_id)

    # Add and Commit the record in the table
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)

    # Return created Interview
    return db_interview

def destroy_interview(db: Session, id: int):
    """
    Delete the interview with given interview id

    :param db: Existing database session
    :param id: Id of the interview to be deleted

    :returns result: Integer status of deletion
    """

    # Build and Commit the delete query
    res = db.query(models.Interview).filter(models.Interview.id == id).delete()
    db.commit()

    # Return the integer status of deletion
    return res

def put_interview(db: Session, new_interview: models.Interview):
    """
    Update the interview with given interview schema

    :param db: Existing database session
    :param new_interview: Schema of the new interview

    """

    # Build and Commit the update query by merging the record
    res = db.merge(new_interview)
    db.commit()
    return res
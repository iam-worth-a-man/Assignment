from fastapi.testclient import TestClient

import os
from .main import app
from . import models

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load key-value pairs from .env file
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

models.Base.metadata.create_all(bind=engine)


with engine.connect() as conn:
    with open("./test.sql", "r", encoding="utf-8") as fp:
        lines = fp.readlines()
        for line in lines:
            print(line.strip())
            query = text(line.strip())
            conn.execute(query)
        conn.commit()

client = TestClient(app)

def test_read_candidate():
    res = client.get("/candidate/1")
    assert res.status_code == 200
    assert res.json() == {
  "name": "vardhman",
  "email": "vardhman@gmail.com",
  "status": "pre-hire",
  "id": 1
}

def test_read_candidates_all():
    res = client.get("/candidates/")
    assert res.status_code == 200
    assert res.json() == [
  {
    "name": "vardhman",
    "email": "vardhman@gmail.com",
    "status": "pre-hire",
    "id": 1
  },
  {
    "name": "aman",
    "email": "aman@gmail.com",
    "status": "active",
    "id": 2
  },
  {
    "name": "soham",
    "email": "soham@gmail.com",
    "status": "inactive",
    "id": 3
  }
]

def test_read_candidates_name():
    res = client.get("/candidates/?name=vardhman")
    assert res.status_code == 200
    assert res.json() == [
  {
    "name": "vardhman",
    "email": "vardhman@gmail.com",
    "status": "pre-hire",
    "id": 1
  }
]

def test_read_candidates_email():
    res = client.get("/candidates/?email=aman@gmail.com")
    assert res.status_code == 200
    assert res.json() == [{
    "name": "aman",
    "email": "aman@gmail.com",
    "status": "active",
    "id": 2
  }]

def test_read_candidates_status():
    res = client.get("/candidates/?status=active")
    assert res.status_code == 200
    assert res.json() == [{
    "name": "aman",
    "email": "aman@gmail.com",
    "status": "active",
    "id": 2
  }]

def test_read_candidates_name_email():
    res = client.get("/candidates/?name=vardhman&email=vardhman@gmail.com")
    assert res.status_code == 200
    assert res.json() == [{
    "name": "vardhman",
    "email": "vardhman@gmail.com",
    "status": "pre-hire",
    "id": 1
  }]

def test_read_candidates_name_status():
    res = client.get("/candidates/?name=vardhman&status=pre-hire")
    assert res.status_code == 200
    assert res.json() == [{
    "name": "vardhman",
    "email": "vardhman@gmail.com",
    "status": "pre-hire",
    "id": 1
  }]

def test_read_candidates_email_status():
    res = client.get("/candidates/?email=soham@gmail.com&status=inactive")
    assert res.status_code == 200
    assert res.json() == [{
    "name": "soham",
    "email": "soham@gmail.com",
    "status": "inactive",
    "id": 3
  }]

def test_create_candidate():
    response = client.post("/candidate", json={
  "name": "jashan",
  "email": "jashan@gmail.com",
  "status": "active"
    })
    assert response.status_code == 201
    assert response.json() == {
  "id":4,
  "name": "jashan",
  "email": "jashan@gmail.com",
  "status": "active"
    }

def test_delete_candidate():
    res = client.delete("/candidate/4")
    assert res.status_code == 200
    assert res.json() == {"detail":"Candidate Deleted Successfully"}


def test_delete_candidate_by_email():
    res = client.delete("/candidate/?email=soham@gmail.com")
    assert res.status_code == 200
    assert res.json() == {"detail":"Candidate Deleted Successfully"}


def test_update_candidate():
    res = client.put("/candidate/2", json={
  "name": "aman S",
  "email": "amanS@gmail.com",
  "status": "active"
    })
    assert res.status_code == 200
    assert res.json() == {"detail":"Candidate Updated Successfully"}


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



def test_read_employee():
    res = client.get("/employee/1")
    assert res.status_code == 200
    assert res.json() == {
  "name": "jatin",
  "email": "jatin@gmail.com",
  "designation": "CEO",
  "id": 1
}

def test_read_employees_all():
    res = client.get("/employees/")
    assert res.status_code == 200
    assert res.json() == [
  {
    "name": "jatin",
    "email": "jatin@gmail.com",
    "designation": "CEO",
    "id": 1
  },
  {
    "name": "jayam",
    "email": "jayam@gmail.com",
    "designation": "Developer",
    "id": 2
  },
  {
    "name": "mayank",
    "email": "mayankD@gmail.com",
    "designation": "Designer",
    "id": 3
  },
  {
    "name": "manu",
    "email": "manu@gmail.com",
    "designation": "Designer",
    "id": 4
  }
]

def test_read_employees_name():
    res = client.get("/employees/?name=jatin")
    assert res.status_code == 200
    assert res.json() == [{
    "name": "jatin",
    "email": "jatin@gmail.com",
    "designation": "CEO",
    "id": 1
  }]

def test_read_employees_email():
    res = client.get("/employees/?email=jatin@gmail.com")
    assert res.status_code == 200
    assert res.json() == [{
    "name": "jatin",
    "email": "jatin@gmail.com",
    "designation": "CEO",
    "id": 1
  }]

def test_read_employees_designation():
    res = client.get("/employees/?designation=CEO")
    assert res.status_code == 200
    assert res.json() == [{
    "name": "jatin",
    "email": "jatin@gmail.com",
    "designation": "CEO",
    "id": 1
  }]

def test_read_employees_name_email():
    res = client.get("/employees/?name=jayam&email=jayam@gmail.com")
    assert res.status_code == 200
    assert res.json() == [{
    "name": "jayam",
    "email": "jayam@gmail.com",
    "designation": "Developer",
    "id": 2
  }]

def test_read_employees_name_designation():
    res = client.get("/employees/?name=jayam&designation=Developer")
    assert res.status_code == 200
    assert res.json() == [{
    "name": "jayam",
    "email": "jayam@gmail.com",
    "designation": "Developer",
    "id": 2
  }]

def test_read_employees_email_designation():
    res = client.get("/employees/?email=jayam@gmail.com&designation=Developer")
    assert res.status_code == 200
    assert res.json() == [{
    "name": "jayam",
    "email": "jayam@gmail.com",
    "designation": "Developer",
    "id": 2
  }]

def test_create_employee():
    response = client.post("/employee", json={
  "name": "ansh",
  "email": "ansh@gmail.com",
  "designation": "Developer"
    })
    assert response.status_code == 201
    assert response.json() == {
    "id":5,
  "name": "ansh",
  "email": "ansh@gmail.com",
  "designation": "Developer"
    }

def test_delete_employee():
    res = client.delete("/employee/4")
    assert res.status_code == 200
    assert res.json() == {"detail":"Employee Deleted Successfully"}


def test_delete_employee_by_email():
    res = client.delete("/employee/?email=ansh@gmail.com")
    assert res.status_code == 200
    assert res.json() == {"detail":"Employee Deleted Successfully"}


def test_update_employee():
    res = client.put("/employee/3", json={
    "name": "mayank",
    "email": "mayank@gmail.com",
    "designation": "Designer"
  })
    assert res.status_code == 200
    assert res.json() == {"detail":"Employee Updated Successfully"}


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



def test_read_interview():
    res = client.get("/interview/1")
    assert res.status_code == 200
    assert res.json() == {
    "round": 1,
    "candidate_id": 1,
    "employee_id": 1,
    "id": 1
  }

def test_read_interviews_all():
    res = client.get("/interviews/")
    assert res.status_code == 200
    assert res.json() == [
  {
    "round": 1,
    "candidate_id": 1,
    "employee_id": 1,
    "id": 1
  },
  {
    "round": 1,
    "candidate_id": 2,
    "employee_id": 2,
    "id": 2
  },
  {
    "round": 2,
    "candidate_id": 1,
    "employee_id": 2,
    "id": 3
  },
  {
    "round": 3,
    "candidate_id": 1,
    "employee_id": 3,
    "id": 4
  }
]

def test_read_interviews_candidate_id():
    res = client.get("/interviews/?candidate_id=1")
    assert res.status_code == 200
    assert res.json() == [
  {
    "round": 1,
    "candidate_id": 1,
    "employee_id": 1,
    "id": 1
  },
  {
    "round": 2,
    "candidate_id": 1,
    "employee_id": 2,
    "id": 3
  },
  {
    "round": 3,
    "candidate_id": 1,
    "employee_id": 3,
    "id": 4
  }
]

def test_read_interviews_employee_id():
    res = client.get("/interviews/?employee_id=1")
    assert res.status_code == 200
    assert res.json() == [
  {
    "round": 1,
    "candidate_id": 1,
    "employee_id": 1,
    "id": 1
  }
]

def test_read_interviews_round():
    res = client.get("/interviews/?round=1")
    assert res.status_code == 200
    assert res.json() == [
  {
    "round": 1,
    "candidate_id": 1,
    "employee_id": 1,
    "id": 1
  },
  {
    "round": 1,
    "candidate_id": 2,
    "employee_id": 2,
    "id": 2
  }
]

def test_read_interviews_candidate_id_employee_id():
    res = client.get("/interviews/?candidate_id=2&employee_id=2")
    assert res.status_code == 200
    assert res.json() == [{
    "round": 1,
    "candidate_id": 2,
    "employee_id": 2,
    "id": 2
  }]

def test_read_interviews_employee_id_round():
    res = client.get("/interviews/?employee_id=2&round=1")
    assert res.status_code == 200
    assert res.json() == [{
    "round": 1,
    "candidate_id": 2,
    "employee_id": 2,
    "id": 2
  }]

def test_read_interviews_candidate_id_round():
    res = client.get("/interviews/?candidate_id=2&round=1")
    assert res.status_code == 200
    assert res.json() == [{
    "round": 1,
    "candidate_id": 2,
    "employee_id": 2,
    "id": 2
  }]

def test_create_interview():
    response = client.post("/interview", json={
  "round": 4,
  "candidate_id": 2,
  "employee_id": 1
    })

    assert response.status_code == 201
    assert response.json() == {
        "id": 5,
  "round": 4,
  "candidate_id": 2,
  "employee_id": 1
    }


def test_delete_interview():
    res = client.delete("/interview/5")
    assert res.status_code == 200
    assert res.json() == {"detail":"Interview Deleted Successfully"}


def test_update_interview():
    res = client.put("/interview/3", json={
  "round": 3,
  "candidate_id": 2,
  "employee_id": 3
    })
    assert res.status_code == 200
    assert res.json() == {"detail":"Interview Updated Successfully"}


# =====================================================
# NEGATIVE TESTS
# =====================================================


def test_read_non_existent_candidate():
    res = client.get("/candidate/100")
    assert res.status_code == 404
    assert res.json() == {"detail":"Candidate not found"}


def test_read_non_existent_candidates_name():
    res = client.get("/candidates/?name=vardhmanjain")
    assert res.status_code == 404
    assert res.json() == {"detail":"Candidate not found"}

def test_read_non_existent_candidates_email():
    res = client.get("/candidates/?email=vjain@gmail.com")
    assert res.status_code == 404
    assert res.json() == {"detail":"Candidate not found"}

def test_read_non_existent_candidates_status():
    res = client.get("/candidates/?status=foo")
    assert res.status_code == 404
    assert res.json() == {"detail":"Candidate not found"}

def test_read_non_existent_candidates_name_email():
    res = client.get("/candidates/?name=vardhmanjain&email=vjain@gmail.com")
    assert res.status_code == 404
    assert res.json() == {"detail":"Candidate not found"}

def test_read_non_existent_candidates_name_status():
    res = client.get("/candidates/?name=vardhmanjain&status=pre")
    assert res.status_code == 404
    assert res.json() == {"detail":"Candidate not found"}

def test_read_non_existent_candidates_email_status():
    res = client.get("/candidates/?email=kartik@gmail.com&status=hi")
    assert res.status_code == 404
    assert res.json() == {"detail":"Candidate not found"}

def test_create_candidate_with_existing_email():
    response = client.post("/candidate", json={
  "name": "jayam",
  "email": "vardhman@gmail.com",
  "status": "In-progress"
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Email already registered"
    }

def test_create_candidate_with_empty_name():
    response = client.post("/candidate", json={
  "name": "",
  "email": "newuser@gmail.com",
  "status": "In-progress"
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Please enter the candidate name"
    }

def test_create_candidate_with_empty_email():
    response = client.post("/candidate", json={
  "name": "newuser",
  "email": "",
  "status": "In-progress"
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Please enter the candidate email"
    }

def test_create_candidate_with_empty_status():
    response = client.post("/candidate", json={
  "name": "newuser",
  "email": "newuser@gmail.com",
  "status": ""
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Please enter the candidate status"
    }

def test_delete_non_existent_candidate():
    res = client.delete("/candidate/100")
    assert res.status_code == 404
    assert res.json() == {"detail":"Candidate not found"}

def test_delete_candidate_with_scheduled_interview():
    res = client.delete("/candidate/1")
    assert res.status_code == 400
    assert res.json() == {"detail":"Candidate can not be deleted as its interview is scheduled"}


def test_delete_candidate_by_non_existent_email():
    res = client.delete("/candidate/?email=random@gmail.com")
    assert res.status_code == 404
    assert res.json() == {"detail":"Candidate not found"}

def test_delete_candidate_by_email_with_scheduled_interview():
    res = client.delete("/candidate/?email=vardhman@gmail.com")
    assert res.status_code == 400
    assert res.json() == {"detail":"Candidate can not be deleted as its interview is scheduled"}


def test_update_non_existent_candidate():
    res = client.put("/candidate/100", json={
  "name": "jayam S",
  "email": "jayam@gmail.com",
  "status": "In-progress"
    })
    assert res.status_code == 404
    assert res.json() == {"detail":"Candidate not found"}

def test_update_candidate_with_empty_name():
    response = client.put("/candidate/1", json={
  "name": "",
  "email": "newuser@gmail.com",
  "status": "In-progress"
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Please enter the candidate name"
    }

def test_update_candidate_with_empty_email():
    response = client.put("/candidate/1", json={
  "name": "newuser",
  "email": "",
  "status": "In-progress"
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Please enter the candidate email"
    }

def test_update_candidate_with_empty_status():
    response = client.put("/candidate/1", json={
  "name": "newuser",
  "email": "newuser@gmail.com",
  "status": ""
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Please enter the candidate status"
    }


def test_update_candidate_with_existing_email():
    response = client.put("/candidate/2", json={
  "name": "jayam",
  "email": "vardhman@gmail.com",
  "status": "In-progress"
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Candidate with the provided email already exists"
    }


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



def test_read_non_existent_employee():
    res = client.get("/employee/100")
    assert res.status_code == 404
    assert res.json() == {"detail":"Employee not found"}


def test_read_non_existent_employees_name():
    res = client.get("/employees/?name=vardhmanjain")
    assert res.status_code == 404
    assert res.json() == {"detail":"Employee not found"}

def test_read_non_existent_employees_email():
    res = client.get("/employees/?email=vjain@gmail.com")
    assert res.status_code == 404
    assert res.json() == {"detail":"Employee not found"}

def test_read_non_existent_employees_designation():
    res = client.get("/employees/?designation=foo")
    assert res.status_code == 404
    assert res.json() == {"detail":"Employee not found"}

def test_read_non_existent_employees_name_email():
    res = client.get("/employees/?name=vardhmanjain&email=vjain@gmail.com")
    assert res.status_code == 404
    assert res.json() == {"detail":"Employee not found"}

def test_read_non_existent_employees_name_designation():
    res = client.get("/employees/?name=vardhmanjain&designation=pre")
    assert res.status_code == 404
    assert res.json() == {"detail":"Employee not found"}

def test_read_non_existent_employees_email_designation():
    res = client.get("/employees/?email=kartik@gmail.com&designation=hi")
    assert res.status_code == 404
    assert res.json() == {"detail":"Employee not found"}

def test_create_employee_with_existing_email():
    response = client.post("/employee", json={
  "name": "jayam",
  "email": "jatin@gmail.com",
  "designation": "Designer"
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Employee with the provided email already exists"
    }

def test_create_employee_with_empty_name():
    response = client.post("/employee", json={
  "name": "",
  "email": "newuser@gmail.com",
  "designation": "Designer"
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Please enter the employee name"
    }

def test_create_employee_with_empty_email():
    response = client.post("/employee", json={
  "name": "newuser",
  "email": "",
  "designation": "Designer"
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Please enter the employee email"
    }

def test_create_employee_with_empty_status():
    response = client.post("/employee", json={
  "name": "newuser",
  "email": "newuser@gmail.com",
  "designation": ""
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Please enter the employee designation"
    }

def test_delete_non_existent_employee():
    res = client.delete("/employee/100")
    assert res.status_code == 404
    assert res.json() == {"detail":"Employee not found"}

def test_delete_employee_with_scheduled_interview():
    res = client.delete("/employee/1")
    assert res.status_code == 400
    assert res.json() == {"detail":"Employee can not be deleted as its an interviewer"}


def test_delete_employee_by_non_existent_email():
    res = client.delete("/employee/?email=random@gmail.com")
    assert res.status_code == 404
    assert res.json() == {"detail":"Employee not found"}

def test_delete_employee_by_email_with_scheduled_interview():
    res = client.delete("/employee/?email=jatin@gmail.com")
    assert res.status_code == 400
    assert res.json() == {"detail":"Employee can not be deleted as its an interviewer"}


def test_update_non_existent_employee():
    res = client.put("/employee/100", json={
  "name": "jayam S",
  "email": "jayam@gmail.com",
  "designation": "Designer"
    })
    assert res.status_code == 404
    assert res.json() == {"detail":"Employee not found"}

def test_update_employee_with_empty_name():
    response = client.put("/employee/1", json={
  "name": "",
  "email": "newuser@gmail.com",
  "designation": "Designer"
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Please enter the employee name"
    }

def test_update_employee_with_empty_email():
    response = client.put("/employee/1", json={
  "name": "newuser",
  "email": "",
  "designation": "Designer"
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Please enter the employee email"
    }

def test_update_employee_with_empty_designation():
    response = client.put("/employee/1", json={
  "name": "newuser",
  "email": "newuser@gmail.com",
  "designation": ""
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Please enter the employee designation"
    }


def test_update_employee_with_existing_email():
    response = client.put("/employee/2", json={
  "name": "jayam",
  "email": "jatin@gmail.com",
  "designation": "Designer"
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Employee with the provided email already exists"
    }

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



def test_read_non_existent_interview():
    res = client.get("/interview/100")
    assert res.status_code == 404
    assert res.json() == {"detail":"Interview not found"}


def test_read_interviews_with_non_existent_candidate_id():
    res = client.get("/interviews/?candidate_id=50")
    assert res.status_code == 404
    assert res.json() == {"detail":"Interview not found"}

def test_read_interviews_with_non_existent_employee_id():
    res = client.get("/interviews/?employee_id=50")
    assert res.status_code == 404
    assert res.json() == {"detail":"Interview not found"}

def test_read_interviews_with_non_existent_round():
    res = client.get("/interviews/?round=100")
    assert res.status_code == 404
    assert res.json() == {"detail":"Interview not found"}

def test_read_interviews_with_non_existent_candidate_id_employee_id():
    res = client.get("/interviews/?candidate_id=50&employee_id=50")
    assert res.status_code == 404
    assert res.json() == {"detail":"Interview not found"}

def test_read_interviews_with_non_existent_candidate_id_round():
    res = client.get("/interviews/?candidate_id=50&round=100")
    assert res.status_code == 404
    assert res.json() == {"detail":"Interview not found"}

def test_read_interviews_with_non_existent_employee_id_round():
    res = client.get("/interviews/?employee_id=40&round=100")
    assert res.status_code == 404
    assert res.json() == {"detail":"Interview not found"}

def test_create_interview_with_existing_candidate_employee():
    response = client.post("/interview", json={
  "round": 2,
  "candidate_id": 1,
  "employee_id": 1
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Interview already scheduled"
    }

def test_create_interview_with_empty_round():
    response = client.post("/interview", json={
  "round": 0,
  "candidate_id": 2,
  "employee_id": 3
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Please enter non-zero round"
    }

def test_create_interview_with_empty_candidate():
    response = client.post("/interview", json={
  "round": 1,
  "candidate_id": 0,
  "employee_id": 1
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Please enter the non-zero candidate id"
    }

def test_create_interview_with_empty_employee():
    response = client.post("/interview", json={
  "round": 1,
  "candidate_id": 1,
  "employee_id": 0
    })
    assert response.status_code == 400
    assert response.json() == {
    "detail":"Please enter the non-zero employee id"
    }


def test_delete_non_existent_interview():
    res = client.delete("/interview/100")
    assert res.status_code == 404
    assert res.json() == {"detail":"Interview not found"}


def test_update_non_existent_interview():
    res = client.put("/interview/100", json={
  "round": 4,
  "candidate_id": 2,
  "employee_id": 2
    })
    assert res.status_code == 404
    assert res.json() == {"detail":"Interview not found"}

def test_update_interview_with_non_existent_candidate():
    res = client.put("/interview/1", json={
  "round": 4,
  "candidate_id": 200,
  "employee_id": 2
    })
    assert res.status_code == 400
    assert res.json() == {"detail":"Candidate to be interviewed is not registered"}

def test_update_interview_with_non_existent_employee():
    res = client.put("/interview/1", json={
  "round": 4,
  "candidate_id": 1,
  "employee_id": 200
    })
    assert res.status_code == 400
    assert res.json() == {"detail":"Employee as Interviewer is not available"}
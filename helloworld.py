from fastapi import FastAPI,Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int
    gender: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

students:Student = {
    1:{
        "name":"Malindu Upendra",
        "age":"25",
        "gender":"Male"
    },
    2:{
        "name":"Dilan Perera",
        "age":"23",
        "gender":"Male"
    },
    3:{
        "name":"Arosh Segar",
        "age":"23",
        "gender":"Male"
    },
    4:{
        "name":"Sandaru Manilka",
        "age":"24",
        "gender":"Male"
    },
}

@app.get("/name")
def getName():
    return {"name":"Malindu Upendra"}

@app.get("/get_student/{studentId}")
def getStudent(studentId: int = Path(None, description="The ID of the studemts you want",gt=0,lt=5)):
    return students[studentId]

@app.get("/get_student_by_name/{studentId}")
def getStudentByName(*, studentId: int,name: Optional[str] = None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"message": "Student not found"}

@app.post("/createStudent/{studentID}")
def create_student(studentID: int, student: Student):
    if studentID in students:
        return {"error": "Student already exist"}
    else:
        students[studentID] = student
        return students

@app.put("/updateStudent/{studentID}")
def update_student(studentID: int,student: UpdateStudent):
    if studentID not in students:
        return {"error": "student does not exist"}
    else:
        if student.name != None:
            students[studentID]["name"] = student.name

        if student.age != None:
            students[studentID]["age"] = student.age

        if student.gender != None:
            students[studentID]["gender"] = student.gender
        
        return students

@app.delete("/deleteStudent/{studentID}")
def delete_student(studentID:int):
    if studentID not in students:
        return {"error": "student does nt exist"}
    else:
        del students[studentID]
        return students
 
from fastapi import FastAPI, HTTPException, Depends,Query
from sqlalchemy.orm import Session
from models.models import Job as JobModel
from schema.Schema import Job
from database import get_db
from routes.auth import router
from utils.auth_bearer import get_current_user
from models.models import User as UserModel
from sqlalchemy import or_,func


app = FastAPI()

app.include_router(router)

#root API
@app.get("/")
async def root():
    return {"message": "Welcome to the Job Board, Find your Dream job!"}


@app.post("/add_job/", status_code=201)
def add_job(
    job: Job,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    new_job = JobModel(title=job.title, description=job.description, salary=job.salary)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return {"message": "Job added successfully", "by": current_user.email}

#display Jobs API
@app.get("/all_jobs", response_model=list[Job], status_code=200)
async def get_all_jobs(
    skip : int = Query(0),
    limit: int = Query(10),
    keyword : str = None,
    min_salary : float = None,
    max_salary : float = None,
    db: Session = Depends(get_db)):
   
    query = db.query(JobModel)
    if keyword:
        query = query.filter(func.lower(JobModel.title).like(f"%{keyword.lower()}%"))

    if min_salary:
        query= query.filter(JobModel.salary >= min_salary)

    if max_salary:
        query = query.filter(JobModel.salary <= max_salary)

    
    jobs = query.offset(skip).limit(limit).all()

    return jobs

#update job
@app.put("/update_job/{id}", status_code=200)
async def update_job(id: int, new_job: Job,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)):
    job = db.query(JobModel).filter(JobModel.id == id).first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {id} not found!")

    job.title = new_job.title
    job.description = new_job.description
    job.salary = new_job.salary
    db.commit()
    return {"message": f"Job {id} updated successfully!"}

#delete Job
@app.delete("/delete_job/{id}", status_code=200)
async def delete_job(id: int, db: Session = Depends(get_db), 
    current_user: UserModel= Depends(get_current_user)):
    job = db.query(JobModel).filter(JobModel.id == id).first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {id} not found!")

    db.delete(job)
    db.commit()
    return {"message": f"Job {id} deleted successfully!"}





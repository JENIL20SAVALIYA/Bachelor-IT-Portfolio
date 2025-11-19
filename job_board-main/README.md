# 🧰 Job Board

A simple Python web app for managing job listings with user authentication, email notifications, and token-based access control.

---

## 🚀 Tech Stack

- **Backend**: [Python](https://www.python.org/), [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)

---

## 📦 Setup Instructions

1. Clone the repository:
 
   git clone https://github.com/kevalmathiya11/job_board.git
   cd job-board
2.Create and activate a virtual environment (optional but recommended):

  python -m venv env
  source env/bin/activate  # On Windows: env\Scripts\activate

3.Install dependencies:
  pip install -r requirements.txt

4.Run the development server:
  uvicorn main:app --reload

## 🔐 Features:

 --> User Signup

Sends a confirmation email upon successful registration.

--> User Login

Returns a JWT token for authorized access to job management routes.

--> Job Management

add_job: Add a new job listing (requires login).

update_job: Update an existing job (requires login).

delete_job: Delete a job listing (requires login).

show_all_jobs: View all job listings with pagination and filtering support.

---

# job_board-main

A simple job board application with authentication and email features.

## Features
- User authentication
- Job posting and management
- Email notifications

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the main app:
   ```bash
   python main.py
   ```



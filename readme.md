# Interview Topics & Pricing Backend

A FastAPI backend for managing interview topics, experience ranges, pricing tables, premium adjustments, and final price calculation.

---

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL (Docker)
- Pydantic
- Python 3.9+

---

## Project Structure

.
├── app/
│ ├── models/ # SQLAlchemy models
│ ├── routers/ # API routers
│ ├── schemas/ # Pydantic schemas & enums
│ ├── db.py # Database configuration & get_db
│ ├── main.py # FastAPI entry point
│ ├── createtableonce.py # One-time DB table creation script
│ └── init.py
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md


---

## Setup Instructions

1️ Clone the repository

```bash
git clone https://github.com/Lokesh-get-git/topics_prices_backend
cd interview-backend

2️ Create & activate virtual environment

python -m venv env
env\Scripts\activate

3️ Install dependencies

pip install -r requirements.txt

4️ Configure environment variables

Create .env from the example file:
copy .env.example .env

Contents of .env:

DATABASE_URL=postgresql+psycopg2://admin:password@localhost:5432/interview_database

5️ Start PostgreSQL (Docker)

docker-compose up -d

Verify:
docker ps

6️ Create database tables (one-time)

alembic upgrade head

IMPORTANT: Experience ranges must be inserted manually after this step.

7️ Start the FastAPI server

From the project root:
uvicorn app.main:app --reload

Server runs at:
http://127.0.0.1:8000

API Documentation

Once running:
Swagger UI
http://127.0.0.1:8000/docs

OpenAPI JSON
http://127.0.0.1:8000/openapi.json

Common Commands

Stop PostgreSQL:
docker-compose down

Stop PostgreSQL and delete data:
docker-compose down -v

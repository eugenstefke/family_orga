# **Family Orga API**

A REST API to organize family life: manage family members, 
events and doctors in one place. Built with FastAPI, PostgreSQL and SQLAlchemy 
as a final project of my Python backend training.

Live demo: coming soon (Render) · Interactive API docs: /docs

### Features
* User registration and login with JWT authentication
* Passwords are stored as secure hashes (never in plain text)
* Manage family members (children, adults, pets) with details like birthday, height, weight, allergies and sizes
* Manage events and link them to the family members who attend
* Manage doctors and link them to the family members they treat
* Every user only sees and changes their own data
* Input validation (e-mail format, password rules, value ranges) with clear error messages
* Automatic interactive documentation (Swagger UI)

### Tech stack

**Area**	            **Technology**
Language	        Python 3.10+
Web framework	    FastAPI
Database	        PostgreSQL
ORM	                SQLAlchemy
Validation	        Pydantic
Authentication	    JWT (HS256), password hashing with pwdlib
Local database	    Docker

### **Architecture**

The project uses three layers and the Repository Pattern, so each part has one job:

Request -> Route -> Service -> Repository -> Database

**Layer**	            **Job**
Routes (routes/)	    Receive the HTTP request, return the response and the right status code
Services (services/)	Business logic (checks, rules, error cases)
Repositories            The only place that talks to the database
(repositories/)	

Each repository has an interface (abstract class) and 
a SQLAlchemy implementation. The services only know the interface, 
so the database access can be exchanged without changing the business logic.

.
├── main.py                 # App entry point, registers all routers
├── auth/                   # JWT creation and current-user dependency
├── data/
│   └── database.py         # Engine, session, Base, get_db()
├── models/
│   └── models.py           # SQLAlchemy models (tables)
├── schemas/                # Pydantic schemas (request/response data)
├── routes/                 # API endpoints
├── services/               # Business logic
└── repositories/           # Database access (interface + SQLAlchemy)

### **Data model**

* User has many FamilyMembers, Events and Doctors
* Event and FamilyMember are linked many-to-many (who attends which event)
* Doctor and FamilyMember are linked many-to-many (who is treated by which doctor)
* Deleting a user also deletes all of their data (cascade delete)

### API endpoints

Authenticated routes need the header **Authorization: Bearer <token>**.

### User

**Method	            Path	                    Description	                                Auth**
POST	            /user/registration	        Create a new user	                        no
POST	            /user/login	                Log in and get a JWT access token	        no
GET	                /user/me	                Show the logged-in user	                    yes
PUT	                /user/details/change	    Change name, e-mail and password	        yes
DELETE	            /user/delete	            Delete the user (password required)	        yes

### Family members

**Method	            Path	                    Description**
GET	                /get/all/familymembers	    List all family members
GET	                /familymember/{id}	        Show details of one family member
POST	            /familymember/create	    Create a family member
PUT	                /familymember/{id}	        Update a family member
DELETE	            /familymember/{id}	        Delete a family member

### Events

**Method	            Path	                    Description**
GET	                    /get/all/events	        List all events
GET	                    /event/{id}	            Show details of one event incl. attending family members
POST	                /event/create	        Create an event and link family members
PUT	                    /event/{id}	            Update an event and its linked family members
DELETE	                /event/{id}	            Delete an event

### Doctors

**Method	                Path	                Description**
GET	                    /get/all/doctors	    List all doctors
GET	                    /doctor/{id}	        Show details of one doctor incl. linked family members
POST	                /doctor/add	            Add a doctor and link family members
PUT	                    /doctor/{id}	        Update a doctor and its linked family members
DELETE	                /doctor/{id}	        Delete a doctor

### Status codes

**Code	Meaning**
200	    Success
400	    A given family member ID does not exist or belongs to another user
401	    Wrong e-mail/password, wrong old password, or missing/invalid token
404	    The requested resource does not exist (or belongs to another user)
409	    Conflict, e.g. e-mail already in use or duplicate family member (same name and birthday)
422	    Invalid input data (e.g. weak password, invalid e-mail format)

### Getting started (local setup)
1. **Clone the repository and install dependencies**

bash:
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

2. **Start a PostgreSQL database**

With Docker:

bash:
docker run --name family-orga-db \
  -e POSTGRES_USER=<db_user> \
  -e POSTGRES_PASSWORD=<db_password> \
  -e POSTGRES_DB=family_orga \
  -p 5432:5432 \
  -v family-orga-data:/var/lib/postgresql/data \
  -d postgres:16

3. **Configure the environment**

Create a **.env** file in the project root (it is listed in **.gitignore** and must never be committed):

env:

DATABASE_URL=postgresql://<db_user>:<db_password>@localhost:5432/family_orga
JWT_SECRET_KEY=<a long random string> (the secure secret key)
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

**Generate a secure secret key with:**

bash:
python -c "import secrets; print(secrets.token_hex(32))"

4. **Create the database tables**

Run this once from the project root:

bash:
python -c "import models.models; from data.database import Base, engine; Base.metadata.create_all(engine)"

5. **Start the API**

bash:
uvicorn main:app --reload

Open http://127.0.0.1:8000/docs to try out all endpoints in the interactive Swagger UI.

### Example workflow

1. POST  /user/registration with name, e-mail and password
2. POST  /user/login with e-mail and password, which returns an access_token
3. Send the token in the Authorization: Bearer <token> header
4. POST /familymember/create to add a family member, then use their ID for events and doctors

_**Password rules: at least 8 characters and at least one special character.**_

### Deployment

Planned: deployment on Render with a managed PostgreSQL database. 
The environment variables DATABASE_URL, JWT_SECRET_KEY, JWT_ALGORITHM and JWT_EXPIRE_MINUTES 
are set in the Render dashboard. Start command: uvicorn main:app --host 0.0.0.0 --port $PORT

### Roadmap

 Deployment on Render
 Automated build/test pipeline with GitHub Actions
 Database migrations with Alembic
 Automated tests with pytest

## Author

Eugen Stefke
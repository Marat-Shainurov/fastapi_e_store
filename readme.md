# General description.
_'fastapi_store_api'_ is a fastapi project.\
The project is a backend part of the **e-store service for authorized users**.\

# Running the project
1. install docker to your local machine if you have not already:
   https://docs.docker.com/get-docker/

2. Clone the project https://github.com/Marat-Shainurov/fastapi_store in your IDE.

3. Build a new image and run the project container from the root project directory:
   - docker-compose build
   - docker-compose up

4. Read the project's documentation (swagger or redoc format):
   - http://127.0.0.1:8000/docs/
   - http://127.0.0.1:8000/redoc/

5. Go to the main page on your browser http://127.0.0.1:8000/docs and start working with the app's endpoints.


# Project structure
1. /app/database/ - package with main database settings. Postgres is used as the database.
2. /app/routes/ - package with project endpoints.
3. /app/schemas/ - package with pydentic schemas.
4. /app/models/ - package with the ORM models. SQLAlchemy is used for the database access.
5. /app/services/ - package with the project service functions.
6. /tests/ - testing package.
7. /main.py - main project file, where the FatsAPI app is instantiated.
8. /requirements.txt - main project dependencies.

# Testing
All the endpoints are covered by pytest tests in /tests/test_main.py

# Security
CORSMiddleware settings are added to the app in main.py.

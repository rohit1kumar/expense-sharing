# Daily Expense Share API

## features
1. User Management
    - singup with email, name, mobile and password.
    - Retrieve profile details.
    - JWT based authentication with proper authorization.
2. Expense Management
    - Add expense with support for split methods: Equal, Exact, and Percentage
    - View individual and overall expense summaries.
    - Download balance sheet csv.


## Tech Stack
- Django Rest Framework
- PostgreSQL

## Database Design
![Database Design](docs/db_design.svg)

## Setup & Runing
1. Clone the repository `git clone https://github.com/rohit1kumar/expense-sharing.git`
2. Create a `.env` using `cp .env.example .env` and update the values.
3. Install dependencies using Poetry `poetry install` or `pip install -r requirements.txt`
4. Run the server using `python manage.py runserver`

5. (Optional) Run using Docker
```bash
docker-compose up --build
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### [API Documentation](docs/api_docs.md)

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/20980024-01bfda48-3b9e-475e-937d-f01829d3b60f?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D20980024-01bfda48-3b9e-475e-937d-f01829d3b60f%26entityType%3Dcollection%26workspaceId%3Dfb130ba8-5a6b-4e2e-96df-3c87dd829d25)
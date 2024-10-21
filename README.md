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

### [API Documentation](docs/api_docs.md)

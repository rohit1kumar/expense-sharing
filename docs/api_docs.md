## API Documentation
User
- Signup

    `POST` /api/v1/users

    Request Body:
    ```json
    {
        "email": "John@gmail.com",
        "password": "password",
        "name": "John Doe", # optional
        "mobile_number": "1234567890" # optional
    }
    ```
    Response:

    ```json
    {
        "id": "fa128ed0-8479-4ce6-ae38-0a724c011ee6",
        "email": "John@gmail.com",
        "name": "John Doe",
        "mobile_number": "1234567890",
        "created_at": "2021-09-12T12:00:00Z"
    }
    ```


- Login

    `POST` /api/v1/token

    Request Body:
    ```json
    {
        "email": "John@gmail.com",
        "password": "password",
    }
    ```
    Resposne:
    ```json
    {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2V"
    }
    ```

- Profile

    `GET` /api/v1/users/current_user

    Request Header:
    ```
    Authorization: Bearer <access_token>
    ```

    Response:
    ```json
    {
       "id": "fa128ed0-8479-4ce6-ae38-0a724c011ee6",
        "email": "John@gmail.com",
        "name": "John Doe",
        "mobile_number": "1234567890",
        "created_at": "2021-09-12T12:00:00Z"
    }

    ```

Expense
- Add Expense

    `POST` /api/v1/expenses

    Request Header:
    ```
    Authorization Bearer <access_token>
    ```

    Request Body:
    ```json
    {
        "title": "Dinner @CP",
        "description": "Dinner with friends",
        "total_amount": "1000",
        "split_type": "EQUAL",
        "splits": [
            {
                "user": "4626e2b7-5a37-4c6a-9bdf-43f3df524e05",
                "percentage": null,
                "amount": "500"
            },
            {
                "user": "43622e4a-5681-4cfe-ba51-a475e991dc2e",
                "percentage": null,
                "amount": "500"
            }
        ]
    }

    ```
    **Note**
    - `split_type`: `EQUAL`, `EXACT`, `PERCENTAGE`
    - `EQUAL`: only user IDs in `splits` are required.
    - `EXACT`: user IDs and amounts in `splits` are required.
    - `PERCENTAGE`: user IDs and percentages in `splits` (sum of percentages should be 100).



- Retrieve individual user expenses

    `GET` /api/v1/expenses/my_expenses

    Request Header:
    ```
    Authorization Bearer <access_token>
    ```
    Response:
    ```json
    {
        "balance_summary": {
            "to_pay": 500.0,
            "to_receive": 0.0,
        },
        "splits": {
            "receive_from": [
                {
                    "date": "2024-10-21 02:34 PM",
                    "expense_id": "2e3b6d67-b4b8-44f5-8202-be3bf072b620",
                    "title": "Goa Trip",
                    "user_email": "Sonu@gmail.com",
                    "user_name": "sonu",
                    "amount": 5000.00
                }
            ],
            "pay_to": [
                {
                    "date": "2024-10-21 02:34 PM",
                    "expense_id": "2e3b6d67-b4b8-44f5-8202-be3bf072b620",
                    "title": "Dinner @MacD",
                    "user_email": "aman@gmail.com",
                    "user_name": "aman",
                    "amount": 500.0
                }
            ]
        }
    }
    ```

- Retrieve overall expenses

    `GET` /api/v1/expenses/overall-expenses

    Request Header:
    ```
    Authorization Bearer <access_token>
    ```
    Response:
    ```json
    {
        "to_pay": 500.0,
        "to_receive": 0.0,
        "net_balance": -500.0
    }
    ```

- Download balance sheet (CSV)

    `GET` /api/v1/expenses/download-balance-sheet

    Request Header:
    ```
    Authorization Bearer <access_token>
    ```

    Response: Sample [CSV file](expense_share.csv)
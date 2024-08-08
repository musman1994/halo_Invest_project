# Trading API Project

## Overview

This project provides a trading API that allows users to manage stocks, place orders, and interact with their trading data. The API uses JWT authentication for secure access and includes endpoints for stock and order management, as well as bulk trade placement.

## Features

1. Stock Management**: Create and retrieve stocks.
2. Order Management**: Place and retrieve orders.
3. Bulk Trade Placement**: Import trades in bulk from a CSV file.

## Installation

### Prerequisites

- Python 3.12
- Django 5.1
- Django REST framework
- Requests library
- Pytest
- Postman

# Halo Invest Project

## Setup

Follow these steps to set up and run the project on your local machine:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/musman1994/halo_Invest_project.git
    cd halo_Invest_project
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # For macOS/Linux
    # For Windows: venv\Scripts\activate
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up Configuration:**

    Create a file named `config.ini` in the root directory.

    ```ini
    [auth]
    Username & Password
    ```

5. **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Start the Django development server:**

    ```bash
    python manage.py runserver
    ```
   
## Creating a Superuser

To manage Django project via the admin interface, you'll need to create a superuser. There are two ways to do this:

### 1. Using the Command Line

You can create a superuser by running the following command:

```bash
python manage.py createsuperuser
```

This command will prompt you to enter a username, email, and password for the superuser. Once created, you'll be able to log in to the Django admin interface.

### 2. Using the Admin Interface

Alternatively, if you prefer to create a user via the admin interface, follow these steps:
- Start your Django development server by running:
```bash
python manage.py runserver
```
- Open your browser and navigate to: http://127.0.0.1:8000/admin/

- Log in using the superuser account you've created via the command line, or use another admin account if available.

- Once logged in, navigate to the "Users" section and create a new user with admin rights by checking the "Staff status" and "Superuser status" options.

## API Endpoints

### Stock Management

- **POST /api/stocks/**: Create a new stock
- **GET /api/stocks/**: List all stocks

### Order Management

- **POST /api/orders/**: Place a new order
- **GET /api/orders/**: List all orders

### Bulk Trade Placement

- **POST /api/place_trades_in_bulk/**: Import trades from a CSV file

## Authentication

### Obtaining a JWT Token

Use Postman to obtain a JWT token:

1. Send a POST request to `/api/token/` with the following body:

    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```

2. In the response, you will receive a token.

### Using the JWT Token

Include the JWT token in the `Authorization` header of your requests. You must send the token as a `Bearer` token to access protected endpoints. 

- **Header**: `Authorization: Bearer YOUR_JWT_TOKEN`

For example, when making a GET or POST request, include the token in the headers:

curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testUser", "password": "testPassword"}'




# Running Tests

To run tests using `pytest`, use:

```bash
pytest tests.py
```

## Setting Up a Cron Job

To automate the execution of the `place_trades_in_bulk.bat` script , follow these steps:

1. **Ensure the Script is in the Repository**

   The `place_trades_in_bulk.bat` script has been included in the project repository.

2. **Open the Crontab Editor**

   Open the crontab editor by running:

```bash
crontab -e
0 * * * * place_trades_in_bulk.bat
```
   
**Save and Exit**

Save the changes and exit the editor. The cron job is now scheduled and will automatically run the script every hour.

**Note:** The place_trades_in_bulk.bat script is intended to insert bulk data from data.csv into the database. Ensure that data.csv is correctly placed and accessible for the script to function properly.  



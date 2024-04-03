# wherebnb-accounts

# Flask Application Setup and Deployment

This repository contains a Flask application that allows you to manage user accounts. Below are the instructions to set up and deploy the application.

## Prerequisites

Before you begin, ensure you have the following installed / set up:

- Python 3.x
- Docker (if you want to containerize the application)
- MySQL server

## Getting Started

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up the environment variables by creating a `.env` file in the root directory with the following content:

    ```plaintext
    PASSWORD=your_mysql_password
    PUBLIC_IP_ADDRESS=your_public_ip_address
    DBNAME=your_database_name
    PROJECT_ID=your_project_id
    INSTANCE_NAME=your_instance_name
    DEBUG=True
    PORT=5000
    ```

    Replace the placeholders with your actual database credentials.

4. Run the Flask application:

    ```bash
    python account.py
    ```

    The application should now be running locally at `http://localhost:5000`.

## Docker Deployment

To deploy the application using Docker, follow these steps:

1. Build the Docker image:

    ```bash
    docker build -t <dockerid>/account:1.0 ./
    ```

2. Run the Docker container:

    ```bash
    docker run -p 5000:5000 --env-file .env -e dbURL=mysql+mysqldb://root:PASSWORD@PUBLIC_IP_ADDRESS/DBNAME?unix_socket=/cloudsql/PROJECT_ID:INSTANCE_NAME <dockerid>/account:1.0
    ```

    Replace `.env` with the path to your `.env` file containing the environment variables.

## Usage

Once the application is running, you can access the following endpoints:

- `/add`: Add a new user account (POST request)
- `/view_all`: View all user accounts (GET request)
- `/view/<id>`: View details of a specific user account by account id (GET request)


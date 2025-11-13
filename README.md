# Sensor Data Dashboard

This is a full-stack web application featuring a Flask backend for managing sensor data and a React frontend for displaying it.

## Features

- **Backend**: A RESTful API built with Python and Flask.
- **Frontend**: A responsive user interface built with React and Vite.
- **Authentication**: JWT-based authentication for secure endpoints.
- **Database**: SQLAlchemy ORM with a SQLite database.
- **API Documentation**: Interactive API documentation using Flasgger (Swagger).

## Project Structure

```
/
├── backend/         # Flask API
├── frontend/        # React Application
└── README.md        # This file
```

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- [Python](https://www.python.org/downloads/) (version 3.8 or higher)
- [Node.js](https://nodejs.org/en/download/) (version 18.x or higher) and npm

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Backend Setup (Flask)

First, let's get the backend server running.

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create and activate a virtual environment:**
    - On Windows:
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create an environment file:**
    Create a new file named `.env` inside the `backend` directory and add a secret key for JWT.

    ```
    JWT_SECRET_KEY=your-super-secret-and-random-key
    ```
    > **Note:** Replace `your-super-secret-and-random-key` with a long, random string for security.

5.  **Run the backend server:**
    ```bash
    python main.py
    ```
    The Flask server will start on `http://127.0.0.1:5000`. The first time you run it, it will automatically create a `contact.db` file and populate it with initial seed data.

    You can access the API documentation at `http://127.0.0.1:5000/api/docs/`.

### 2. Frontend Setup (React)

Now, let's set up the frontend client. Open a **new terminal window** for this part.

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

3.  **Run the frontend development server:**
    ```bash
    npm run dev
    ```

4.  **Access the application:**
    Open your web browser and navigate to the URL provided by Vite (usually `http://localhost:5173`).


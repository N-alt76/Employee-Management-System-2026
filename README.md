# Employee Management System

A simple web application for managing employee records through a browser-based dashboard and REST API.

## Features

- View all employees in the management dashboard
- Add new employees with validation for required fields, email uniqueness, and salary values
- Edit existing employee records
- Delete employees
- REST API endpoints for employee management
- SQLite database for lightweight local persistence

## Technologies Used

- Python
- Flask
- SQLite
- HTML, CSS, and JavaScript

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/N-alt76/Employee-Management-System-2026.git
   cd Employee-Management-System-2026
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows:

   ```bash
   .venv\Scripts\activate
   ```

   macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the project:

   ```bash
   python main.py
   ```

5. Open `http://localhost:5000` in your browser.

## Deployment

This project includes a `render.yaml` blueprint for deployment on Render.

1. Push the repository to GitHub.
2. In Render, choose **New > Blueprint** and select this repository.
3. Render installs the dependencies and starts the app with Gunicorn on the platform-provided port.
4. Set `SECRET_KEY` in Render if you want to replace the generated value.

The default SQLite database is stored in the deployment filesystem. On free hosting, that filesystem may be reset during redeployments or restarts; use a persistent disk or external database when production data must survive.


## Author

Nilesh Jadhav

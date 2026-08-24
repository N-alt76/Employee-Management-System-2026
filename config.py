from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "employees.db"
SECRET_KEY = "employee-management-development-key"

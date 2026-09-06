import os
import secrets
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = Path(os.environ.get("DATABASE_DIR", BASE_DIR))
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_PATH = DATABASE_DIR / "employees.db"
SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

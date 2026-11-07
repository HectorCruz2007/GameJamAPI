import os

# Settings with safe defaults for local development
SECRET_KEY = os.getenv("GAMEJAM_SECRET_KEY", "dev-only-secret-key-change-me-0123456789")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = int(os.getenv("GAMEJAM_TOKEN_MINUTES", "10080"))  # 7 days
DATABASE_URL = os.getenv("GAMEJAM_DATABASE_URL", "sqlite:///./gamejam.db")

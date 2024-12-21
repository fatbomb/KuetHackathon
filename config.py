import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # EXTERNAL_URL = os.getenv("EXTERNAL_URL")
    LLM_URL = os.getenv("LLM_URL")
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    OCR_API_URL = os.getenv("OCR_API_URL")
    OCR_API_KEY = os.getenv("OCR_API_KEY")

import os

class Config:

    SECRET_KEY = "student_secret_key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///student_management.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

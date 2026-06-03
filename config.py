class Config:

    # ==================================
    # SECRET KEY
    # ==================================

    SECRET_KEY = "student_secret_key"

    # ==================================
    # SQLITE DATABASE
    # ==================================

    SQLALCHEMY_DATABASE_URI = "sqlite:///school.db"

    # ==================================
    # SQLALCHEMY TRACK MODIFICATIONS
    # ==================================

    SQLALCHEMY_TRACK_MODIFICATIONS = False
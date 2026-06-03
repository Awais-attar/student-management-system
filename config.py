class Config:


SECRET_KEY = "student_secret_key"

SQLALCHEMY_DATABASE_URI = (
    "mysql+pymysql://root:1111@localhost/student_management"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False


from decouple import config

SECRET_KEY = config('JWT_SECRET_KEY', "")
REFRESH_SECRET_KEY = config('JWT_REFRESH_SECRET_KEY')
DB_NAME = config('DB_NAME', 'test')
DB_HOST = config('DB_HOST', 'localhost')
DB_PORT = config('DB_PORT', 3306)
DB_PASSWORD = config('DB_PASSWORD', '11111111')
DB_USER = config('DB_USER', 'root')
DB_DIALECT = config('DB_DIALECT', "mysql+mysqldb")
DATABASE_URL = f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

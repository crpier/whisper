set -gx APP_PORT "80"
set -gx SQLALCHEMY_DATABASE_URI "mariadb+pymysql://root:changethislol@127.0.0.1:3306/app"
set -gx FIRST_SUPERUSER_EMAIL "todo@example.com"
set -gx FIRST_SUPERUSER_NAME "admin"
set -gx FIRST_SUPERUSER_PASSWORD "todo"
set -gx PYTHONPATH .

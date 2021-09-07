from os import getenv

DATABASE_URI = getenv("DATABASE_URI", "sqlite://db.sqlite3")

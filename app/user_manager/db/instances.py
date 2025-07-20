from app.user_manager.db.user import UserDatabase

DATABASE_URL = "postgresql://myuser:mypassword@postgres-service:5432/mydb"

user_db = UserDatabase(DATABASE_URL, force_rollback=False)


def get_user_database() -> UserDatabase:
    return user_db


async def connect_database():
    await user_db.connect()


async def disconnect_database():
    await user_db.disconnect()

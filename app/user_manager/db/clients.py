from app.user_manager.db.user import UserDatabaseClient

DATABASE_URL = "postgresql://myuser:mypassword@postgres-service:5432/mydb"

user_db = UserDatabaseClient(DATABASE_URL, force_rollback=False)


def get_user_db() -> UserDatabaseClient:
    return user_db


async def connect_database():
    await user_db.connect()


async def disconnect_database():
    await user_db.disconnect()

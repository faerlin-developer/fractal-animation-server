from common.db.sql.client import UserDatabase
from user_manager.config import cfg

user_db = UserDatabase(cfg.database_url, force_rollback=False)


def get_user_db() -> UserDatabase:
	return user_db


async def connect_database():
	await user_db.connect()


async def disconnect_database():
	await user_db.disconnect()

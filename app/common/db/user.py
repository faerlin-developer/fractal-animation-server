from fastapi import HTTPException

from app.common.db.base import BaseDatabaseClient
from app.common.tables.user import Users


class BaseUserDatabaseClient(BaseDatabaseClient):

	def __init__(self, database_url, force_rollback=False):
		super().__init__(database_url, force_rollback)

	async def get_user(self, username):
		query = Users.select().where(Users.c.username == username)
		return await self.database.fetch_one(query)


async def verify_user(username: str, user_db: BaseUserDatabaseClient):
	""""""

	user = await user_db.get_user(username)

	if user is None:
		raise HTTPException(status_code=409, detail="username does not exists")

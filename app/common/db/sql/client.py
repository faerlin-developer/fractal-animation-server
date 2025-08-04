import databases

from common.db.sql.tables.task import Tasks, State
from common.db.sql.tables.user import Users


class BaseDatabase:

	def __init__(self, database_url, force_rollback=False):
		self.database = databases.Database(database_url, force_rollback=force_rollback)

	async def connect(self):
		await self.database.connect()

	async def disconnect(self):
		await self.database.disconnect()


class TaskDatabase(BaseDatabase):

	def __init__(self, database_url, force_rollback=False):
		super().__init__(database_url, force_rollback)

	async def add(self, username: str, z_re: float, z_im: float, state: State) -> int:
		query = Tasks.insert().values(username=username, z_re=z_re, z_im=z_im, state=state)
		return await self.database.execute(query)

	async def update_state(self, task_id, state: State):
		query = (
			Tasks.update()
			.where(Tasks.c.id == task_id)
			.values(state=state.value)
		)
		await self.database.execute(query)

	async def get_task(self, task_id):
		query = Tasks.select().where(Tasks.c.id == task_id)
		return await self.database.fetch_one(query)

	async def get_tasks(self, username: str):
		pass


class UserDatabase(BaseDatabase):

	def __init__(self, database_url, force_rollback=False):
		super().__init__(database_url, force_rollback)

	async def create_user(self, username, password_hash):
		query = Users.insert().values(username=username, password_hash=password_hash)
		return await self.database.execute(query)

	async def get_user(self, username):
		query = Users.select().where(Users.c.username == username)
		return await self.database.fetch_one(query)

	async def delete_user(self, username):
		query = Users.delete().where(Users.c.username == username)
		return await self.database.execute(query)

	async def execute(self, query):
		return await self.database.execute(query=query)

	async def verify_user(self, username: str):
		user = await self.get_user(username)
		return user is not None

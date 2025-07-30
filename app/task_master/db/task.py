from app.common.db.base import BaseDatabaseClient
from app.common.tables.task import State
from app.common.tables.task import Tasks


class TaskDatabaseClient(BaseDatabaseClient):

    def __init__(self, database_url, force_rollback=False):
        super().__init__(database_url, force_rollback)

    async def add(self, username: str, z_re: float, z_im: float, state: State) -> int:
        query = Tasks.insert().values(username=username, z_re=z_re, z_im=z_im, state=state)
        return await self.database.execute(query)

    async def update_state(self, task_id, state: str):
        pass

    async def get_tasks(self, username: str):
        pass

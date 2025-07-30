import databases


class BaseDatabaseClient:

    def __init__(self, database_url, force_rollback=False):
        self.database = databases.Database(database_url, force_rollback=force_rollback)

    async def connect(self):
        await self.database.connect()

    async def disconnect(self):
        await self.database.disconnect()

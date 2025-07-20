import databases

from app.common.tables.user import Users


class UserDatabase:

    def __init__(self, database_url, force_rollback=False):
        self.database = databases.Database(database_url, force_rollback=force_rollback)

    async def connect(self):
        await self.database.connect()

    async def disconnect(self):
        await self.database.disconnect()

    async def get_user(self, username):
        query = Users.select().where(Users.c.username == username)
        return await self.database.fetch_one(query)

    async def create_user(self, username, password_hash):
        query = Users.insert().values(username=username, password_hash=password_hash)
        return await self.database.execute(query)

    async def delete_user(self, username):
        query = Users.delete().where(Users.c.username == username)
        return await self.database.execute(query)

    async def execute(self, query):
        return await self.database.execute(query=query)

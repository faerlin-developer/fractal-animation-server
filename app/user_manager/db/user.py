from app.common.db.user import BaseUserDatabaseClient
from app.common.tables.user import Users


class UserDatabaseClient(BaseUserDatabaseClient):

    def __init__(self, database_url, force_rollback=False):
        super().__init__(database_url, force_rollback)

    async def create_user(self, username, password_hash):
        query = Users.insert().values(username=username, password_hash=password_hash)
        return await self.database.execute(query)

    async def delete_user(self, username):
        query = Users.delete().where(Users.c.username == username)
        return await self.database.execute(query)

    async def execute(self, query):
        return await self.database.execute(query=query)

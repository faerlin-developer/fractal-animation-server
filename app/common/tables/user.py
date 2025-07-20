from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, func

metadata = MetaData()

Users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=False, unique=True),
    Column('password_hash', String, nullable=False),
    Column('created_at', TIMESTAMP, server_default=func.now())
)

from enum import StrEnum

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, func, Float

metadata = MetaData()


class State(StrEnum):
	READY = "READY"
	RUNNING = "RUNNING"
	DONE = "DONE"
	FAILED = "FAILED"


Tasks = Table(
	'tasks',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('username', String, nullable=False),
	Column('z_re', Float, nullable=False),
	Column('z_im', Float, nullable=False),
	Column('state', String, nullable=False),
	Column('created_at', TIMESTAMP, server_default=func.now())
)

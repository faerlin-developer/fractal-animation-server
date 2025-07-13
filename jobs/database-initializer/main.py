from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table

DATABASE_URL = "postgresql://myuser:mypassword@postgres-service:5432/mydb"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
)

metadata.create_all(engine)

print("Tables created.")

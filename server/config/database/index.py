from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config.constants.index import database_url

Base = declarative_base()

engine = create_async_engine(database_url)
Session = async_sessionmaker(engine)

async def get_db() : 
    async with Session() as session : 
        yield session

async def initalize_database():
    print("Hello from initalize database")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)



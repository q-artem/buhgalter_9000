from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base

from database.models import Language

DATABASE_URL = "sqlite+aiosqlite:///./bot.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        async with session.begin():
            languages = [
                {"code": "ru", "name": "Русский"},
                {"code": "en", "name": "English"},
            ]
            for lang in languages:
                if not await session.get(Language, lang["code"]):
                    session.add(Language(**lang))
            await session.commit()
""""
session.py -> file that manages how your application talks to the database.
It defines the connection machinery: how connections are created, 
pooled, reused, and safely handed to each request.

Without this file, every route that needs the DB would have to manually open a connection, 
run a query, and close the connection — every single time, with no shared pooling, 
no consistent configuration, and high risk of leaking connections (forgetting to close them) 
or misconfiguring something differently in different routes.
"""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from auth_service.core import settings

# engine - one persistent connection pool for the whole applicaion,
# not a single open connection. It's a factory + pool manager that 
# knows how to open connections to your database (using the driver 
# specified in the URL — here, aiosqlite), and it maintains a small 
# pool of them so your app isn't paying the cost of opening a 
# brand-new TCP/file connection on every single query.
# You create the engine once, at module import time, and the 
# entire app shares this one instance for its whole lifetime.
async_engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)

# AsyncSessionLocal — a factory that hands out fresh, isolated sessions for each request
# A session is a short-lived, per-request "workspace" — it borrows a connection from the pool, 
# tracks every object you load/add/modify during that unit of work, and handles translating 
# your Python-level changes into SQL statements when you commit(). You create a brand new 
# session for every request, use it, then throw it away — you never share one session across 
# multiple concurrent requests, because sessions aren't safe for concurrent use and mixing 
# unrelated requests' data into one session would cause serious bugs (e.g. one request seeing another's uncommitted changes).
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

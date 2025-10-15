from __future__ import annotations

from typing import NoReturn, Optional, cast

import asyncpg
from cassandra import cluster as scy_cluster
from redis.asyncio import Redis
from starlette.concurrency import run_in_threadpool

from app.settings import settings


class Resources:
    pg_pool: Optional[asyncpg.Pool] = None
    redis: Optional[Redis] = None
    scylla_session: Optional[scy_cluster.Session] = None
    scylla_cluster: Optional[scy_cluster.Cluster] = None


resources = Resources()


def _uninit(name: str) -> NoReturn:
    raise RuntimeError(f"{name} not initialized")


def get_pg_pool() -> asyncpg.Pool:
    if resources.pg_pool is None:
        _uninit("pg_pool")
    return cast(asyncpg.Pool, resources.pg_pool)


def get_redis() -> Redis:
    if resources.redis is None:
        _uninit("redis")
    return cast(Redis, resources.redis)


def get_scylla_session() -> scy_cluster.Session:
    if resources.scylla_session is None:
        _uninit("scylla_session")
    return cast(scy_cluster.Session, resources.scylla_session)


async def init_pg():
    resources.pg_pool = await asyncpg.create_pool(
        host=settings.PG_HOST,
        port=settings.PG_PORT,
        user=settings.PG_USER,
        password=settings.PG_PASSWORD,
        database=settings.PG_DB,
        min_size=1,
        max_size=5,
    )


async def close_pg():
    if resources.pg_pool:
        await resources.pg_pool.close()


def init_redis():
    resources.redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)


async def close_redis():
    if resources.redis:
        await resources.redis.close()


async def init_scylla():
    def _connect():
        cluster = scy_cluster.Cluster(settings.SCYLLA_HOSTS.split(","))
        session = cluster.connect(settings.SCYLLA_KEYSPACE)
        return cluster, session

    resources.scylla_cluster, resources.scylla_session = await run_in_threadpool(
        _connect
    )


async def close_scylla():
    if resources.scylla_session:
        await run_in_threadpool(resources.scylla_session.shutdown)
    if resources.scylla_cluster:
        await run_in_threadpool(resources.scylla_cluster.shutdown)


async def ping_pg() -> bool:
    pool = get_pg_pool()
    async with pool.acquire() as conn:
        val = await conn.fetchval("SELECT 1;")
        return val == 1


async def ping_redis() -> bool:
    pong = await get_redis().ping()
    return bool(pong)


async def ping_scylla() -> bool:
    def _ping():
        rows = get_scylla_session().execute("SELECT key FROM system.local;")
        return True if rows else True

    return await run_in_threadpool(_ping)

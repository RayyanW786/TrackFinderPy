from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from contextlib import asynccontextmanager
import asyncio
from typing import Dict, Any

from app.deps import (
    init_pg,
    close_pg,
    init_redis,
    close_redis,
    init_scylla,
    close_scylla,
    ping_pg,
    ping_redis,
    ping_scylla,
)


def rust_version() -> str:
    try:
        import trackfinder_py as tf

        return tf.version()
    except Exception as e:
        return f"unavailable: {e.__class__.__name__}: {e}"


async def health(_req):
    results: Dict[str, Any] = {
        "status": "ok",
        "rust": rust_version(),
    }
    pg_ok, redis_ok, scy_ok = await asyncio.gather(
        ping_pg(), ping_redis(), ping_scylla()
    )
    results["postgres"] = pg_ok
    results["redis"] = redis_ok
    results["scylla"] = scy_ok
    return JSONResponse(results)


@asynccontextmanager
async def lifespan(_app):
    await init_pg()
    init_redis()
    await init_scylla()
    yield

    await close_scylla()
    await close_redis()
    await close_pg()


routes = [Route("/health", health)]
app = Starlette(routes=routes, lifespan=lifespan)

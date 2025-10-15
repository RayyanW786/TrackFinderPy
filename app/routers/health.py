from starlette.responses import JSONResponse


async def health(_request):
    try:
        import trackfinder_py as tf

        rust_version = tf.version()
    except Exception as e:
        rust_version = f"unavailable: {e.__class__.__name__}"

    return JSONResponse(
        {
            "status": "ok",
            "rust": rust_version,
        }
    )

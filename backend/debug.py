print("Tracing fastapi imports:")
try:
    print(" import starlette")
    import starlette
    print(" import pydantic")
    import pydantic
    print(" import anyio")
    import anyio
    print(" import fastapi")
    import fastapi
    print("SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()

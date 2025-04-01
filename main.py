from uvicorn import run
from src.app import app, port, host

if __name__ == "__main__":
    run(
        app=app,
        port=port,
        host=host,
    )



"""
server/app.py — OpenEnv standard entry-point.

openenv validate requires:
  - a main() function in this file
  - if __name__ == '__main__': main()  (so it is callable)
"""

import uvicorn


def main(host: str = "0.0.0.0", port: int = 7860) -> None:
    """Start the FastAPI server via uvicorn."""
    uvicorn.run("server:app", host=host, port=port)


if __name__ == "__main__":
    main()

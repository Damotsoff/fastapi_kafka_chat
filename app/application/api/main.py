from fastapi import FastAPI


def create_app():
    return FastAPI(
        title="SImple Kafka chat",
        docs_url="/api/docs",
        description="A simple Kafka + DDD example.",
        debug=True,
    )

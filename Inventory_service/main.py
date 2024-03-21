from fastapi.routing import APIRoute
from fastapi import FastAPI, APIRouter
from src.inventory.entrypoints import app as app1
import uvicorn


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}_{route.name}"


# Add each router in each app to app.include_routers.
app = FastAPI(generate_unique_id_function=custom_generate_unique_id)
app.include_router(app1.router)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)

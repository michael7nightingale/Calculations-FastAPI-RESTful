from fastapi import APIRouter, Request


main_router = APIRouter(prefix='')


@main_router.get("/")
async def homepage(request: Request):
    """Главная страница"""
    return {"message": "This is main page"}



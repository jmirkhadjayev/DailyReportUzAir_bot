from aiogram import Router

from . import admin, common, employee


def setup_routers() -> Router:
    router = Router(name="root")
    router.include_router(common.router)
    router.include_router(admin.router)
    router.include_router(employee.router)
    return router

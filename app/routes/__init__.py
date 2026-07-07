from fastapi import APIRouter

from .retrieve import router as retrieve_router
from .create import router as create_router

router = APIRouter(prefix="/contacts", tags=["Contacts"])

router.include_router(retrieve_router)
router.include_router(create_router)

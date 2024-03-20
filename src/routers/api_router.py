from fastapi import APIRouter

from .v1.chromosome import router as chromosome_router

router_v1 = APIRouter()

router_v1.include_router(chromosome_router, prefix="/chromosomes", tags=["chromosomes"])

from fastapi import APIRouter

from src.services.chromosome import ChromosomeSerivce

router = APIRouter()
service = ChromosomeSerivce()


@router.get("/")
async def get_chromosome_list():
    return service.get_chromosome_list()


@router.get("/{filename}")
async def get_chromosome_file(filename: str):
    return service.get_chromosome_file(filename)


@router.delete("/{filename}")
async def delete_chromosome_file(filename: str):
    return service.delete_chromosome_file(filename)


from fastapi import BackgroundTasks


@router.post("/")
async def post_chromosome(
    background_tasks: BackgroundTasks, live: int = 20, popu: int = 20, anchor:int = 0
):
    return service.post_chromosome(background_tasks, live, popu)

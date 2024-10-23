from fastapi import APIRouter

from src.services.chromosome import ChromosomeSerivce

router = APIRouter()
service = ChromosomeSerivce()


@router.get("")
async def get_chromosome_list():
    return service.get_chromosome_list()

@router.get("/rule")
async def get_rule():
    return service.get_rule()

@router.get("/evaluate/{filename}")
async def evaluate_chromosome_file(filename: str):
    return service.evaluate_chromosome_file(filename)

@router.get("/detail")
async def get_chromosome_detail():
    return service.get_chromosome_detail()

@router.get("/{filename}")
async def get_chromosome_file(filename: str):
    return service.get_chromosome_file(filename)

@router.delete("/{filename}")
async def delete_chromosome_file(filename: str):
    return service.delete_chromosome_file(filename)



from fastapi import BackgroundTasks


@router.post("")
async def post_chromosome(
    background_tasks: BackgroundTasks,
    live: int = 1000,
    popu: int = 100,
    anchor: int | None = None,
):
    return service.post_chromosome(background_tasks, live, popu)

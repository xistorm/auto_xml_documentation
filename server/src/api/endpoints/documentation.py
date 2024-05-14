from fastapi import APIRouter

from starlette.status import HTTP_200_OK

router = APIRouter()


@router.get(
    '/create',
    status_code=HTTP_200_OK,
)
async def create():
    pass

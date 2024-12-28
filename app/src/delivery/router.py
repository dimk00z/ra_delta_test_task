from typing import Annotated, Iterable, Sequence
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query, Request, status
from fastapi.responses import JSONResponse
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.src.delivery.entities import GetParcelsFilterParams, RegisterParcelDTO
from app.src.delivery.models import Parcel, ParcelType
from app.src.delivery.services.parcels_service import ParcelService
from app.src.users.models import User
from app.src.users.services import UserService

delivery_router = APIRouter(route_class=DishkaRoute)


@delivery_router.get(
    "/parcels",
    tags=["api"],
    response_model=Iterable[ParcelType],
)
async def get_parcels(
    request: Request,
    filter_query: Annotated[GetParcelsFilterParams, Query()],
    user_service: FromDishka[UserService],
    parcel_service: FromDishka[ParcelService],
) -> Iterable[ParcelType]:
    "Returns user parcels"
    user: User = await user_service.get_user(session=request.session)
    parcels: Iterable[Parcel] = await parcel_service.get_parcels(
        user=user,
        filter_query=filter_query,
    )
    return parcels


@delivery_router.get(
    "/parcels/types",
    tags=["api"],
    response_model=list[ParcelType],
)
async def get_parcels_types(
    db_session: FromDishka[AsyncSession],
) -> Sequence[ParcelType]:
    "Returns all parcels type"
    async with db_session as session:
        results = await session.exec(
            select(ParcelType).order_by(ParcelType.name),
        )
    return results.all()


@delivery_router.post(
    "/parcels",
    tags=["api"],
    status_code=status.HTTP_201_CREATED,
)
async def register_parcel(
    request: Request,
    parcel_dto: RegisterParcelDTO,
    user_service: FromDishka[UserService],
    parcel_service: FromDishka[ParcelService],
) -> Parcel:
    "Returns simple object"
    user: User = await user_service.get_user(session=request.session)
    parcel: Parcel = await parcel_service.create_parcel(
        user=user,
        parcel_dto=parcel_dto,
    )
    return parcel


@delivery_router.get("/parcels/{uuid}", tags=["api"])
async def get_parcel(
    uuid: Annotated[UUID, Path(title="Parcel id")],
) -> JSONResponse:
    "Returns simple object"
    return JSONResponse({"ping": "pong!"})

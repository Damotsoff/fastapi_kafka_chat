from application.api.messages.schemas import (
    CreateChatRequestSchema,
    CreateChatResponseSchema,
)
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic import init_container
from logic.commands.messages import CreateChatCommand
from logic.mediator import Mediator
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi import Depends, status

router = APIRouter(
    tags=["Chat"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт создает новый чат, если чат с таким названием существует , то возвращается 400 ошибка.",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_chat_handler(schema: CreateChatRequestSchema,container=Depends(init_container)):
    mediator: Mediator = container.resolve(Mediator)
    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )
    return CreateChatResponseSchema.from_entity(chat=chat)

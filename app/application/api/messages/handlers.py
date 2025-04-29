from typing import Iterable
from punq import Container
from application.api.messages.schemas import (
    ChatDetailsSchema,
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageResponseSchema,
    CreateMessageSchema,
)
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic import init_container
from logic.commands.messages import CreateChatCommand, CreateMessageCommand
from logic.mediator import Mediator
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi import Depends, status

from logic.queries.messages import GetChatDetailQuery

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
async def create_chat_handler(
    schema: CreateChatRequestSchema, container: Container = Depends(init_container)
) -> CreateChatResponseSchema:
    mediator: Mediator = container.resolve(Mediator)
    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )
    return CreateChatResponseSchema.from_entity(chat=chat)


@router.post(
    "/{chat_oid}/messages",
    status_code=status.HTTP_201_CREATED,
    description="ручка на добавление нового сообщения в чат с переданным objectID.",
    responses={
        status.HTTP_201_CREATED: {"model": CreateMessageSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_message_handler(
    chat_oid: str,
    schema: CreateMessageSchema,
    container: Container = Depends(init_container),
) -> CreateMessageResponseSchema:
    mediator: Mediator = container.resolve(Mediator)
    try:
        message, *_ = await mediator.handle_command(
            CreateMessageCommand(text=schema.text, chat_oid=chat_oid)
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )
    return CreateMessageResponseSchema.from_entity(message)


@router.get(
    "/{chat_oid}/",
    status_code=status.HTTP_200_OK,
    description="получить информацию о чате и все сообщения в нем.",
    responses={
        status.HTTP_200_OK: {"model": ChatDetailsSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_chat_with_messages_handler(
    chat_oid, container: Container = Depends(init_container)
) -> ChatDetailsSchema:
    mediator: Mediator = container.resolve(Mediator)
    try:
        chat = await mediator.handle_query(GetChatDetailQuery(chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )
    return ChatDetailsSchema.from_entity(chat)

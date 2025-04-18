from pytest import fixture

from infra.repositories.messages import BaseChatRepository, MemoryChatRepository
from logic import init_mediator
from logic.mediator import Mediator

@fixture(scope='package')
def chat_repository() -> MemoryChatRepository:
    return MemoryChatRepository()




@fixture(scope='package')
def mediator(chat_repository: BaseChatRepository) -> Mediator:
    mediator = Mediator()
    init_mediator(mediator=mediator,chat_repository=chat_repository)
    return mediator


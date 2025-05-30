from dataclasses import dataclass, field
from collections import defaultdict
from typing import Iterable
from domain.events.base import BaseEvent
from logic.commands.base import CR, CT, BaseCommand, CommandHadler
from logic.events.base import ER, ET, EventHandler
from logic.exceptions.mediator import (
    CommandHandlersNotRegisteredException,
    EventHandlersNotRegisteredException,
)
from logic.queries.base import QR, QT, BaseQuery, BaseQueryHandler


@dataclass(eq=False)
class Mediator:
    event_map: dict[ET, EventHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    command_map: dict[CT, CommandHadler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    queries_map: dict[QT, BaseQueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    def register_query(self, query: QT, query_handler: BaseQueryHandler[QT, QR]) -> QR:
        self.queries_map[query] = query_handler

    def register_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]):
        self.event_map[event].append(event_handlers)

    def register_command(
        self, command: CT, command_handlers: Iterable[CommandHadler[CT, CR]]
    ):
        self.command_map[command].extend(command_handlers)

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        event_type = events.__class__
        handlers = self.event_map.get(event_type)
        if not handlers:
            raise EventHandlersNotRegisteredException(event_type)
        result = []
        for event in events:
            result.extend([await handler.handle(event) for handler in handlers])
        return result

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.command_map.get(command_type)
        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)
        return [await handler.handle(command) for handler in handlers]

    async def handle_query(self, query: BaseQuery) -> QR:
        return await self.queries_map[query.__class__].handle(query=query)

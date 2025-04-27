from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from domain.entities.base import BaseEntity
from domain.events.message import NewChatCreated, NewMessageRecievedEvent
from domain.values.messages import Text, Title


@dataclass
class Message(BaseEntity):

    created_at: datetime = field(default_factory=lambda: datetime.now(), kw_only=True)
    text: Text

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: "Message") -> bool:
        return self.oid == __value.oid


@dataclass
class Chat(BaseEntity):
    created_at: datetime = field(default_factory=lambda: datetime.now(), kw_only=True)
    title: str = Title
    messages: set[Message] = field(default_factory=set, kw_only=True)

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: "Chat") -> bool:
        return self.oid == __value.oid

    @classmethod
    def create_chat(cls, title: Title) -> "Chat":
        new_chat = cls(title=title)
        new_chat.register_event(
            NewChatCreated(
                chat_oid=new_chat.oid, title=new_chat.title.as_generic_type()
            )
        )
        return new_chat

    def add_message(self, message: Message):
        self.messages.add(message)
        self.register_event(
            NewMessageRecievedEvent(
                message_text=message.text.as_generic_type(),
                chat_oid=self.oid,
                message_oid=message.oid,
            )
        )

from typing import Any, Mapping
from domain.entities.messages import Chat, Message
from domain.values.messages import Text, Title


def convert_message_to_document(message: Message) -> dict:
    return {
        "oid": message.oid,
        "text": message.text.as_generic_type(),
        "created_at": message.created_at,
    }


def convert_chat_entity_to_document(chat: Chat) -> dict:
    return {
        "oid": chat.oid,
        "created_at": chat.created_at,
        "title": chat.title.as_generic_type(),
        "messages": [convert_message_to_document(message) for message in chat.messages],
    }


def convert_document_to_chat_entity(message_document: Mapping[str, Any]) -> Message:
    return Message(
        text=Text(value=message_document["text"]),
        oid=message_document["oid"],
        created_at=message_document["created_at"],
    )


def convert_chat_document_to_entity(chat_document: Mapping[str, Any]) -> Chat:
    return Chat(
        title=Title(value=chat_document["title"]),
        oid=chat_document["oid"],
        created_at=chat_document["created_at"],
        messages={
            convert_document_to_chat_entity(message_document)
            for message_document in chat_document["messages"]
        },
    )

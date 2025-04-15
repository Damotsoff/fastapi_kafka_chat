from dataclasses import dataclass
from domain.values.messages import Text


@dataclass
class Messages:
    oid: str
    text: Text
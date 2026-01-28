from typing import Optional
from ninja import Schema


class PubSubMessageSchema(Schema):
    data: str  # base64 encoded string
    attributes: Optional[dict[str, str]] = None
    message_id: str
    messageId: str
    publish_time: str
    publishTime: str


class PubSubEnvelopeSchema(Schema):
    message: PubSubMessageSchema
    subscription: str

import logging
from typing import Optional

from google.cloud import pubsub_v1
from injector import inject


logger = logging.getLogger(__name__)


class GCPPubSubPublishService:
    @inject
    def __init__(self, publisher_client: pubsub_v1.PublisherClient, gcp_project_id: str):
        self._publisher_client = publisher_client
        self._gcp_project_id = gcp_project_id

    def _publish_message(
        self, topic_path: str, message: bytes, message_type: Optional[str] = None
    ) -> "pubsub_v1.publisher.futures.Future":
        attrs = {}
        if message_type:
            attrs["message_type"] = message_type
        return self._publisher_client.publish(topic_path, message, **attrs)

    def publish(self, topic_name: str, message: bytes, message_type: Optional[str] = None) -> None:
        topic_path = self._publisher_client.topic_path(self._gcp_project_id, topic_name)
        future = self._publish_message(topic_path, message, message_type)

        def callback(future: "pubsub_v1.publisher.futures.Future") -> None:
            try:
                message_id = future.result()
                logger.info(f"Message published to topic: {topic_name}, message_id: {message_id}")
            except Exception as e:
                logger.error(f"Error publishing message to topic: {topic_name}, error: {e}")

        future.add_done_callback(callback)

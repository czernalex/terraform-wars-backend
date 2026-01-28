import logging

from google.cloud import pubsub_v1
from injector import inject


logger = logging.getLogger(__name__)


class GCPPubSubPublishService:
    @inject
    def __init__(self, publisher_client: pubsub_v1.PublisherClient, gcp_project_id: str):
        self._publisher_client = publisher_client
        self._gcp_project_id = gcp_project_id

    def publish(self, topic_name: str, message: bytes) -> None:
        topic_path = self._publisher_client.topic_path(self._gcp_project_id, topic_name)
        future = self._publisher_client.publish(topic_path, message)

        def callback(future: "pubsub_v1.publisher.futures.Future") -> None:
            try:
                message_id = future.result()
                logger.info(f"Message published to topic: {topic_name}, message_id: {message_id}")
            except Exception as e:
                logger.error(f"Error publishing message to topic: {topic_name}, error: {e}")

        future.add_done_callback(callback)

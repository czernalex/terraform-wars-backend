from typing import Callable

from google.cloud import pubsub_v1
from injector import inject


class GCPPubSubSubscribeService:
    @inject
    def __init__(self, subscriber_client: pubsub_v1.SubscriberClient):
        self._subscriber_client = subscriber_client

    def subscribe(
        self, subscription_path: str, callback: Callable[["pubsub_v1.subscriber.message.Message"], None]
    ) -> None:
        self._subscriber_client.subscribe(subscription_path, callback=callback)

from datetime import timedelta

from google import pubsub_v1
from injector import inject


class GCPPubSubSubscriptionCreateService:
    @inject
    def __init__(self, subscriber_client: pubsub_v1.SubscriberClient):
        self._subscriber_client = subscriber_client

    def _create_subscription(self, topic_path: str, subscription_path: str) -> None:
        create_request = pubsub_v1.Subscription(
            name=subscription_path,
            topic=topic_path,
            expiration_policy=pubsub_v1.ExpirationPolicy(
                ttl=timedelta(days=1),
            ),
        )
        return self._subscriber_client.create_subscription(create_request)

    def create(self, project_id: str, topic_name: str, subscription_name: str) -> pubsub_v1.Subscription:
        topic_path = self._subscriber_client.topic_path(project_id, topic_name)
        subscription_path = self._subscriber_client.subscription_path(project_id, subscription_name)
        return self._create_subscription(topic_path, subscription_path)

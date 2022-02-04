import os


class Component:
    def __init__(self,
        availability_topic: str = '',
        availability_payload_online: str = '',
        availability_payload_offline: str = '',
    ) -> None:
        self.availability_topic = availability_topic
        self.availability_payload_online = availability_payload_online or os.getenv('DEFAULT_AVAILABILITY_PAYLOAD_ONLINE', 'online')
        self.availability_payload_offline = availability_payload_offline or os.getenv('DEFAULT_AVAILABILITY_PAYLOAD_OFFLINE', 'offline')
        self.available = False

    def is_optimistic(self) -> bool:
        return not bool(self.availability_topic)

    def is_available(self) -> bool:
        return self.available or self.is_optimistic()

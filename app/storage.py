from collections import defaultdict
from time import time
from typing import Any, Dict, Optional

import aioboto3
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import (
    BaseStorage,
    DefaultKeyBuilder,
    KeyBuilder,
    StateType,
    StorageKey,
)

events = defaultdict(dict)


class EventStorage:
    DEFAULT_SESSION = aioboto3.Session()

    def __init__(self, table, session=None):
        self._table = table
        self._session = session or self.DEFAULT_SESSION

    @property
    def resource(self):
        return self._session.resource("dynamodb")

    async def add_event(self, key, data):
        session = aioboto3.Session()
        async with session.resource("dynamodb") as resource:
            table = await resource.Table(self._table)
            await table.put_item(
                Item={"user_id": str(key), "timestamp": int(time()), **data}
            )


events = EventStorage("joinme-prod-events")


class DynamoDBStorage(BaseStorage):

    DEFAULT_KEY = "storage_key"
    DEFAULT_SESSION = aioboto3.Session()
    DEFAULT_KEYBUILDER = DefaultKeyBuilder

    def __init__(
        self,
        table: str,
        pk: Optional[str] = None,
        session: Optional[aioboto3.Session] = None,
        key_builder: Optional[KeyBuilder] = None,
    ):
        self._table = table
        self._pk = pk or self.DEFAULT_KEY
        self._session = session or self.DEFAULT_SESSION
        self._builder = key_builder or self.DEFAULT_KEYBUILDER

    @property
    def builder(self):
        return self._builder()

    @property
    def resource(self):
        return self._session.resource("dynamodb")

    def build(self, key, **kwargs):
        return {self._pk: self.builder.build(key), **kwargs}

    async def get_state(self, key: StorageKey) -> Optional[str]:
        async with self.resource as resource:
            table = await resource.Table(self._table)
            response = await table.get_item(Key=self.build(key))
            if item := response.get("Item"):
                return item.get("state") or None

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        async with self.resource as resource:
            table = await resource.Table(self._table)
            await table.update_item(
                Key=self.build(key),
                UpdateExpression="SET #st = :val",
                ExpressionAttributeValues={
                    ":val": getattr(state, "state", state) or ""
                },
                ExpressionAttributeNames={"#st": "state"},
            )

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        async with self.resource as resource:
            table = await resource.Table(self._table)
            response = await table.get_item(Key=self.build(key))
            if item := response.get("Item"):
                return item.get("data") or {}

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        async with self.resource as resource:
            table = await resource.Table(self._table)
            await table.update_item(
                Key=self.build(key),
                UpdateExpression="SET #da = :val",
                ExpressionAttributeValues={":val": data},
                ExpressionAttributeNames={"#da": "data"},
            )

    async def close(self) -> None:
        self._session = None

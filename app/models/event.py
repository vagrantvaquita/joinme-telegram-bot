from datetime import datetime
from time import time
from typing import Annotated

import aioboto3
from pydantic import BaseModel, Field

SUMMARY = """
<i>{which}</i>\n
<b>{title}</b>\n
<b>What:</b> {what}
<b>Where:</b> {where}
<b>When:</b> <u>{when}</u>
<b>URL:</b> {url}
"""

DateTime = Annotated[datetime, Field(exclude=True)]


class Event(BaseModel):
    category: str
    title: str
    description: str
    location: str
    datetime: DateTime
    url: str

    async def add_event(self, user):
        session = aioboto3.Session()
        async with session.resource("dynamodb") as resource:
            table = await resource.Table("joinme-prod-events")
            await table.put_item(
                Item={
                    "user_id": str(user),
                    "timestamp": int(time()),
                    "datetime": int(self.datetime.timestamp()),
                    **self.model_dump(),
                }
            )

    def summary(self):
        return SUMMARY.format(
            which=self.category,
            title=self.title,
            what=self.description,
            where=self.location,
            when=self.datetime.strftime("%c"),
            url=self.url,
        )

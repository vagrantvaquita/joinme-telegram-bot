import asyncio
from typing import Annotated, Dict, List

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from boto3.dynamodb.types import TypeDeserializer
from pydantic import BaseModel, Field, field_validator

from app.callbacks import EventAction
from app.configs import CONFIG_BOT, TOKEN


class Keys(BaseModel):
    user_id: int

    @field_validator("user_id", mode="before")
    def unmarshall(cls, v):
        return int(v["S"])


class DynamoDB(BaseModel):
    Keys: Keys
    NewImage: Dict[str, Annotated[str, Field(coerce_numbers_to_str=True)]]

    @field_validator("NewImage", mode="before")
    def deserialize(cls, v):
        deserializer = TypeDeserializer()
        return {k: deserializer.deserialize(v) for k, v in v.items()}


class Record(BaseModel):
    dynamodb: DynamoDB


class Event(BaseModel):
    Records: List[Record]

    @property
    def user_id(self):
        return self.items["user_id"]

    @property
    def timestamp(self):
        return self.items["timestamp"]

    @property
    def keys(self):
        return {"user_id": self.user_id, "timestamp": self.timestamp}

    @property
    def items(self):
        return self.Records[0].dynamodb.NewImage

    def summary(self):
        return (
            "You just created the following event:\n"
            "<b><a href='{url}'>{title}</a></b>\n\n"
            "<b>Category</b>: {category}\n"
            "<b>Date</b>: {datetime}\n"
            "<b>Location</b>: {location}\n"
            "<b>Description</b>: {description}\n"
        ).format(**self.items)


bot = Bot(token=TOKEN, default=CONFIG_BOT)
loop = asyncio.get_event_loop()


async def feed_raw_update(bot, event):
    await bot.send_message(
        chat_id=event.user_id,
        text=event.summary(),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="❌ Delete",
                        callback_data=EventAction(action="delete", **event.keys).pack(),
                    ),
                ]
            ]
        ),
    )


def notify(event, context):
    event = Event.model_validate(event)
    loop.run_until_complete(feed_raw_update(bot, event))

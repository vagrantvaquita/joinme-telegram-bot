import asyncio
import json

from app.bot import bot, dp

loop = asyncio.get_event_loop()


def entrypoint(fn):
    def wrapper(event, context):
        body = json.loads(event.pop("body"))
        return fn(event, body, context)

    return wrapper


@entrypoint
def handler(request, body, context):
    print(body)
    loop.run_until_complete(dp.feed_raw_update(bot, body))

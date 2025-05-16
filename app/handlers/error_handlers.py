from aiogram.types.error_event import ErrorEvent
import logging

async def global_error_handler(event: ErrorEvent) -> bool:
    logging.exception(f"[Exception] {event.exception} from update: {event.update}")
    return True
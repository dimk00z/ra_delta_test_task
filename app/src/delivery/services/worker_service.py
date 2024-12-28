import asyncio
import json
import logging
from dataclasses import dataclass, field

import aio_pika

from app.config import Settings
from app.src.currency.service import ExchangeRateService
from app.src.delivery.services.parcels_service import ParcelService

logger = logging.getLogger(__name__)


@dataclass
class BackgroundWorkerService:
    settings: Settings
    exchange_service: ExchangeRateService
    parcel_service: ParcelService

    rabbitmq_url: str = field(init=False)
    channel: aio_pika.Channel | None = field(init=False)

    @property
    async def connection(self):
        self._connection = getattr(
            self,
            "_connection",
            None,
        ) or await aio_pika.connect_robust(
            host=self.settings.rabbitmq_host,
            port=self.settings.rabbitmq_port,
            login=self.settings.rabbitmq_user,
            password=self.settings.rabbitmq_password,
        )
        return self._connection

    async def connect(self):
        if self._connection:
            return
        connection = await self.connection
        self.channel = await connection.channel()
        await self.channel.set_qos(prefetch_count=1)

        queue = await self.channel.declare_queue(
            self.settings.queue_name,
            durable=True,
        )

        await queue.consume(self.process_message)

        logger.info("Package worker connected and waiting for messages")

    async def process_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            try:
                body = json.loads(message.body.decode())
                logger.debug(body)
                # TODO implement it
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                # Requeue the message
                await message.reject(requeue=True)

    async def run(self):
        await self.connect()
        try:
            await asyncio.Future()
        finally:
            await self.close()

    async def close(self):
        if not self._connection:
            return
        await self._connection.close()
        self._connection = None
        self._channel = None

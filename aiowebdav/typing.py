from typing import Protocol


class AsyncWriteBuffer(Protocol):

    async def write(self, data: bytes):
        ...

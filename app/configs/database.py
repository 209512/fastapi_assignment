# app/configs/database.py

import gel
from app.configs.base import settings

_client = None

async def get_client():
    global _client
    if _client is None:
        # GelDB 클라이언트 초기화와 연결 (비동기)
        _client = gel.Client(dsn=settings.EDGEDB_DSN)
        await _client.connect()
    return _client
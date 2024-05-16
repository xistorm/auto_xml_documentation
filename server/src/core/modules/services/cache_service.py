import os
import hashlib

from dotenv import load_dotenv
from redis import Redis

from src.models.entities import Entity


load_dotenv()


class CacheService:

    host = os.getenv('REDIS_HOST', 'localhost')
    port = int(os.getenv('REDIS_PORT', 6379))
    redis = Redis(host=host, port=port, db=0)

    @staticmethod
    def _get_key(entity: Entity) -> str:
        hash_object = hashlib.md5()
        text = entity.text.encode('utf-8')
        hash_object.update(text)
        text_hash = hash_object.hexdigest()

        return text_hash

    @staticmethod
    def get(entity: Entity) -> str:
        entity_hash = CacheService._get_key(entity)
        documentation = CacheService.redis.get(entity_hash)
        documentation_text = documentation.decode('utf-8')

        return documentation_text

    @staticmethod
    def add(entity: Entity, documentation: str) -> None:
        entity_hash = CacheService._get_key(entity)
        CacheService.redis.set(entity_hash, documentation)

    @staticmethod
    def has(entity: Entity) -> bool:
        entity_hash = CacheService._get_key(entity)
        has_cache = True if CacheService.redis.exists(entity_hash) else False

        return has_cache

    @staticmethod
    def delete(entity: Entity) -> None:
        entity_hash = CacheService._get_key(entity)
        CacheService.redis.delete(entity_hash)

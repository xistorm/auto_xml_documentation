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
    def _get_key(entity: Entity, language: str) -> str:
        hash_object = hashlib.md5()
        text = entity.text.encode('utf-8')
        hash_object.update(text)
        text_hash = hash_object.hexdigest()
        entity_key = f'{language}_{text_hash}'

        return entity_key

    @staticmethod
    def get(entity: Entity, language: str) -> str:
        entity_hash = CacheService._get_key(entity, language)
        documentation = CacheService.redis.get(entity_hash)
        documentation_text = documentation.decode('utf-8')

        return documentation_text

    @staticmethod
    def add(entity: Entity, documentation: str, language: str) -> None:
        entity_hash = CacheService._get_key(entity, language)
        CacheService.redis.set(entity_hash, documentation)

    @staticmethod
    def has(entity: Entity, language: str) -> bool:
        entity_hash = CacheService._get_key(entity, language)
        has_cache = True if CacheService.redis.exists(entity_hash) else False

        return has_cache

    @staticmethod
    def delete(entity: Entity, language: str) -> None:
        entity_hash = CacheService._get_key(entity, language)
        CacheService.redis.delete(entity_hash)

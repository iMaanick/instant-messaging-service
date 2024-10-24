import redis as redis
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, RedisStrategy

cookie_transport = CookieTransport(cookie_max_age=7200)

redis = redis.asyncio.from_url("redis://localhost:6379", decode_responses=True)


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(redis, lifetime_seconds=7200)


auth_backend = AuthenticationBackend(
    name="redis",
    transport=cookie_transport,
    get_strategy=get_redis_strategy,
)

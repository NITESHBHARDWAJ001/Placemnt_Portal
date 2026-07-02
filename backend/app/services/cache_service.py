"""Phase-2 placeholder.

In Phase 2 this module will wrap Redis (get/set/delete/expire) so that
dashboard stats, drive listings, etc. can be cached transparently.
Every method is a safe no-op in Phase 1 so calling code never needs to
change when Redis is plugged in.
"""


class CacheService:
    enabled = False

    @classmethod
    def get(cls, key):
        return None

    @classmethod
    def set(cls, key, value, ttl_seconds=300):
        return None

    @classmethod
    def delete(cls, key):
        return None

    @classmethod
    def delete_pattern(cls, pattern):
        return None

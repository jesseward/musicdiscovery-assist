import json
import logging

from redis import Redis

from config import cfg
from liblastfm import LastFM


_redis = Redis(host=cfg['REDIS_HOST'], port=cfg['REDIS_PORT'])

logger = logging.getLogger('music-discovery')


class RedisCache(object):
    """Wrapper around Redis to be used to cache results
    from the last.fm API. All Key Values are (de)serialized to JSON during the
    set/get calls."""

    def __init__(self, handle=None):
        self.handle = handle

    def add(self, key, value, timeout=2592000):
        """Persists the key->value pair to Redis. The value can be any type
        that can be serialized to a json string.

        Default key expiry set to 30 days.

        :param key: String representing an object key
        :param value: A Python type that supports JSON serialization."""

        try:
            self.handle.setex(key, json.dumps(value), timeout)
        except Exception as e:
            raise KeyError(e)

    def get(self, key):
        """Retrieves a JSON serialized object from Redis. Also
        de-serializes to the Python object. Our use case will be a str, list
        or dict."""

        try:
            key = json.loads(self.handle.get(key))
	except TypeError as e:
	    raise LookupError('key not found')
        except Exception as e:
            raise LookupError(e)

        return key


def cached_result(func, args, kwargs):
    """Performs a look-up of the cache and on cache miss, initiates call
    to last.fm and populates result for future lookups.

    key is built using the following
    funcname:argsN for example where func='get_similar_tracks' and args=[
    'metro+area', 'caught+up']
    get_similar_tracks:metro+area:caught+up

    The value written to Redis is a serialized JSON object.

    :param func: A string representing a function name from the LastFM class
    :param args: A list of args to pass to func
    :param kwargs: A dict of kwargs to pass to func
    :return: response from the corresponding func method"""

    cache = RedisCache(handle=_redis)
    key = func + ':' + ':'.join(args)

    try:
        logger.debug(u'Looking up key=' + key)
        results = cache.get(key)
    except LookupError as e:
        logger.warn('Failed to retrieve key from cache. key="{0}", error="{1}"'.format(key, e))
        results = None

    if not results:
        logger.debug(key + ' not found in cache. Calling last.fm')
        try:
            lastfm = LastFM(cfg['API_KEY'])
            results = getattr(lastfm, func)(*args, **kwargs)
        except LookupError as e:
            logger.warn('unable to call {0}, error={1}'.format(func, e))
            return results

        try:
            logger.debug(u'Writing key=' + key)
            cache.add(key, results)
        except KeyError as e:
            logger.error('Unable to write key to cache. key="{0}" to cache, error="{1}"'.format(key, e))

    return results

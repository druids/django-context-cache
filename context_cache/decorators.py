from contextlib import ContextDecorator

from functools import _make_key

from .context import context_cache


def cache_calculate_key(fn, *args, **kwargs):
    """
    Calculate the cache key of a function call with args and kwargs
    Taken from lru_cache
    """
    # combine args with kwargs, separated by the cache_args_kwargs_marker

    fn_key = fn.__module__ + '.' + fn.__name__

    return _make_key(
        (fn_key, ) + tuple(args),
        kwargs,
        False
    )

def cache_for_context(fn):
    """
    Decorator that allows to cache a function call with parameters and its result only for the current context cache
    The result is stored in the memory of the current thread
    As soon as the context is destroyed, the cache is destroyed
    """
    def wrapper(*args, **kwargs):
        cache = context_cache

        if not cache.is_active():
            # no cache found -> directly execute function without caching
            return fn(*args, **kwargs)

        # cache found -> check if a result is already available for this function call
        key = cache_calculate_key(fn, *args, **kwargs)
        result = cache.get(key)
        if not result:
            # no result available -> execute function
            result = fn(*args, **kwargs)
            cache.set(key, result)
        return result
    return wrapper


class InitContextCache(ContextDecorator):

    def __enter__(self):
        context_cache.start()

    def __exit__(self, exc_type, exc_value, traceback):
        context_cache.end()


def init_context_cache(fn=None):
    if callable(fn):
        return InitContextCache()(fn)
    else:
        return InitContextCache()

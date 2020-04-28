from django.conf import settings
from django.db.transaction import get_connection

from threading import local

from django.core.signals import request_finished


class ContextCacheError(Exception):
    pass


class ContextCache(local):

    def __init__(self):
        self._clear()
        request_finished.connect(self._request_finished_receiver)

    def _assert_active(self):
        """Checks for an active revision, throwning an exception if none."""
        if not self.is_active():  # pragma: no cover
            raise ContextCacheError('There is no active context cache for this thread')

    def _clear(self):
        self._stack = []

    def _request_finished_receiver(self, **kwargs):
        """
        Called at the end of a request, ensuring that any open cache
        are closed. Not closing all active revisions can cause memory leaks
        and weird behaviour.
        """
        while self.is_active():  # pragma: no cover
            self._clear()

    @property
    def _current_cache(self):
        self._assert_active()
        return self._stack[-1]

    def is_active(self):
        """Returns whether there is an active revision for this thread."""
        return bool(self._stack)

    def set(self, key, val):
        self._assert_active()
        self._current_cache[key] = val

    def get(self, key):
        self._assert_active()
        return self._current_cache.get(key)

    def start(self):
        if self.is_active():
            self._stack.append(self._current_cache.copy())
        else:
            self._stack.append({})

    def end(self):
        self._assert_active()
        self._stack.pop()


context_cache = ContextCache()

from .context import context_cache


class ContextCacheMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        context_cache.start()
        response = self.get_response(request)
        context_cache.end()
        return response

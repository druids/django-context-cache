Prolog
======

`Django-context-cache` extends the Django framework with a context cache that caches data per request or per decorated block.

Installation
------------

- Install `django-context-cache` with the `pip` command:

```bash
pip install django-context-cache
```

- Add `'context_cache.middleware.ContextCacheMiddleware'` to your `MIDDLEWARE`:

```python
MIDDLEWARE = [
    'context_cache.middleware.ContextCacheMiddleware',
    ...
]
```

Usage
-----
Imagine having an function or method which result you want to cache per request:

    import random
    import string
    from context_cache.decorators import cache_for_context
    
    @cache_for_context
    def get_random_string():
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(10))


If you call function get_random_string more times the value will be get from cache:

    def view(request):
        get_random_string() == get_random_string() # should return True

If you want to cache an function out of requests, for example in the django command you can use the decorator `init_context_cache`. The decorator can be used as a context processor too:

    from django.core.management.base import BaseCommand, CommandError
    from context_cache.decorators import init_context_cache
    
    class Command(BaseCommand):
        
        @init_context_cache
        def handle(self, *args, **options):
            get_random_string() == get_random_string() # should return True

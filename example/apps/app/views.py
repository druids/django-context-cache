import random
import string

from context_cache.decorators import cache_for_context

from django.http import HttpResponse, HttpResponseNotFound


@cache_for_context
def get_random_string():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))


def test_view(request):
    random_strings = [
        get_random_string()
        for _ in range(10)
    ]
    return HttpResponse(','.join(random_strings))

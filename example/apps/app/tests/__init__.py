from germanium.test_cases.client import ClientTestCase
from germanium.tools import assert_equal, assert_not_equal

from context_cache.decorators import cache_for_context, init_context_cache


class ContextCacheTestCase(ClientTestCase):

    def test_not_initialized_cache_should_call_cached_method(self):
        not_cached_value = 'test'

        @cache_for_context
        def cached_method():
            return not_cached_value

        assert_equal(cached_method(), 'test')
        not_cached_value = 'test2'
        assert_equal(cached_method(), 'test2')

    def test_initialized_cache_should_not_call_cached_method(self):
        cached_value = 'test'

        @cache_for_context
        def cached_method():
            return cached_value

        with init_context_cache():
            assert_equal(cached_method(), 'test')
            cached_value = 'test2'
            assert_equal(cached_method(), 'test')

    def test_initialized_cache_should_cache_according_to_input_arguments(self):
        cached_value = 'test'

        @cache_for_context
        def cached_method(*args, **kwargs):
            return cached_value

        with init_context_cache():
            assert_equal(cached_method(), 'test')
            cached_value = 'test2'
            assert_equal(cached_method(), 'test')
            assert_equal(cached_method(1), 'test2')
            cached_value = 'test3'
            assert_equal(cached_method(1), 'test2')
            assert_equal(cached_method(2), 'test3')
            assert_equal(cached_method(a=1), 'test3')

    def test_init_context_cache_should_be_hiearchical(self):
        cached_value1 = 'test'
        cached_value2 = 'test2'

        @cache_for_context
        def cached_method1():
            return cached_value1

        @cache_for_context
        def cached_method2():
            return cached_value2

        with init_context_cache():
            assert_equal(cached_method1(), 'test')
            cached_value1 = 'test_2'
            assert_equal(cached_method1(), 'test')
            with init_context_cache():
                assert_equal(cached_method1(), 'test')
                assert_equal(cached_method2(), 'test2')
                cached_value2 = 'test2_2'
                assert_equal(cached_method2(), 'test2')
            assert_equal(cached_method1(), 'test')
            assert_equal(cached_method2(), 'test2_2')

    def test_view_should_return_same_strings(self):
        response = self.get('/')
        assert_equal(len(set(response.content.decode().split(','))), 1)

    def test_two_requests_should_not_return_same_strings(self):
        assert_not_equal(self.get('/').content, self.get('/').content)

from django.conf import settings

TEST_DISCOVER_TOP_LEVEL = getattr(settings, 'TEST_DISCOVER_TOP_LEVEL', None)
TEST_DISCOVER_PATTERN = getattr(settings, 'TEST_DISCOVER_PATTERN', 'test*.py')

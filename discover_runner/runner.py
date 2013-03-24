from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.test.simple import DjangoTestSuiteRunner, reorder_suite
from django.utils.importlib import import_module

from discover_runner.settings import (TEST_DISCOVER_ROOT,
                                      TEST_DISCOVER_TOP_LEVEL,
                                      TEST_DISCOVER_PATTERN)

try:
    from django.utils.unittest import defaultTestLoader
except ImportError:
    try:
        from unittest2 import defaultTestLoader  # noqa
    except ImportError:
        raise ImproperlyConfigured("Couldn't import unittest2 default "
                                   "test loader. Please use Django >= 1.3 "
                                   "or install the unittest2 library.")


class DiscoverRunner(DjangoTestSuiteRunner):
    """
    A test suite runner that uses unittest2 test discovery.
    """
    test_loader = defaultTestLoader
    reorder_by = (TestCase,)

    def __init__(self, discover_root=None, discover_top_level=None,
                 discover_pattern=None, *args, **kwargs):
        super(DiscoverRunner, self).__init__(*args, **kwargs)
        self.discover_root = discover_root or TEST_DISCOVER_ROOT
        self.discover_top_level = discover_top_level or TEST_DISCOVER_TOP_LEVEL
        self.discover_pattern = discover_pattern or TEST_DISCOVER_PATTERN

    def build_suite(self, test_labels, extra_tests=None):
        suite = None
        root = self.discover_root

        if test_labels:
            suite = self.test_loader.loadTestsFromNames(test_labels)
            # if single named module has no tests, do discovery within it
            if not suite.countTestCases() and len(test_labels) == 1:
                suite = None
                root = import_module(test_labels[0]).__path__[0]

        if suite is None:
            suite = self.test_loader.discover(root,
                pattern=self.discover_pattern,
                top_level_dir=self.discover_top_level)

        if extra_tests:
            for test in extra_tests:
                suite.addTest(test)

        return reorder_suite(suite, self.reorder_by)

from optparse import make_option
from django.core.management.commands.test import Command as TestCommand

class Command(TestCommand):
    option_list = TestCommand.option_list + (
        make_option('--root',
            action='store', dest='test_discover_root', default=None,
            help='Overrides the TEST_DISCOVER_ROOT setting.'),
        make_option('--top-level',
            action='store', dest='test_discover_top_level', default=None,
            help='Overrides the TEST_TOP_LEVEL setting.'),
        make_option('--pattern',
            action='store', dest='test_discover_pattern', default=None,
            help='Overrides the TEST_DISCOVER_PATTERN setting.'),
    )
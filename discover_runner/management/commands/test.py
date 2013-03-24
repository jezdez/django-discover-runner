from optparse import make_option
from django.core.management.commands.test import Command as TestCommand

from discover_runner import settings


class Command(TestCommand):
    option_list = TestCommand.option_list + (
        make_option('-r', '--root',
                    action='store', dest='test_discover_root',
                    default=settings.TEST_DISCOVER_ROOT,
                    help='Overrides the TEST_DISCOVER_ROOT setting.'),
        make_option('-t', '--top-level',
                    action='store', dest='test_discover_top_level',
                    default=settings.TEST_DISCOVER_TOP_LEVEL,
                    help='Overrides the TEST_TOP_LEVEL setting.'),
        make_option('-p', '--pattern',
                    action='store', dest='test_discover_pattern',
                    default=settings.TEST_DISCOVER_PATTERN,
                    help='Overrides the TEST_DISCOVER_PATTERN setting.'),
    )

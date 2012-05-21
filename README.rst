django-discover-runner
======================

An alternative Django ``TEST_RUNNER`` which uses the unittest2_ test discovery
from a base path specified in the settings, or any other module or package
specified to the ``test`` management command -- including app tests.

If you just run ``./manage.py test``, it'll discover and run all tests
underneath the ``TEST_DISCOVER_ROOT`` setting (a file system path). If you run
``./manage.py test full.dotted.path.to.test_module``, it'll run the tests in
that module (you can also pass multiple modules). If you give it a single
dotted path to a package (like a Django app) like ``./manage.py test myapp``
and that package does not itself directly contain any tests, it'll do
test discovery in all submodules of that package.

.. note::

    This code uses the default unittest2_ test discovery behavior, which
    only searches for tests in files named ``test*.py``. To override this
    see the ``TEST_DISCOVER_PATTERN`` setting below.

Why?
----

Django's own test discovery is very much tied to the directory structure
of Django apps, partly due to historic reasons (the unittest library
didn't have its own discovery for a long time) and prevents Django app
authors from being good Python citizens. django-discover-runner uses the
official test discovery feature of the new unittest2_ library which is
included in Django.

By default there is no way to put project specific tests in a separate
folder outside the Python package of the Django project, which is a great
way to organize your code, separating the tests and non-test code.
django-discover-runner helps you clean up your project tests.

There is also no way to specify fully dotted import paths to test
modules, functions, class or methods to the ``test`` management command
but only Django's odd standard ``<appname>.<TestClassName>``.
django-discover-runner allows you to specify any type of label to Django's
test management command.

By default Django's test runner will execute the tests of Django's own
contrib apps, which doesn't make sense if you just want to run your
own app's or project's tests. django-discover-runner fixes this by allowing
you to specify which tests to run and organize your test code outside the
reach of the Django test runner.

More reasons can be found in Carl Meyer's excellent talk about
`Testing and Django`_ (slides_).

.. _`Testing and Django`: http://pyvideo.org/video/699/testing-and-django
.. _slides: http://carljm.github.com/django-testing-slides/

Settings
--------

- ``TEST_RUNNER`` (required) needs to point to the ``DiscoverRunner`` class
  to enable it::

    TEST_RUNNER = 'discover_runner.DiscoverRunner'

- ``TEST_DISCOVER_ROOT`` (optional) should be the root directory to discover
  tests within. You could make this the same as ``TEST_DISCOVER_TOP_LEVEL``
  if you want tests to be discovered anywhere in your project or app.

- ``TEST_DISCOVER_TOP_LEVEL`` (optional) should be the directory containing
  your top-level package(s); in other words, the directory that should be on
  ``sys.path`` for your code to import. This is the directory containing
  ``manage.py`` in the new Django 1.4 project layout.

- ``TEST_DISCOVER_PATTERN`` (optional) is the pattern to use when discovering
  tests and defaults to the unittest2_ standard ``test*.py``.

Examples
--------

Django app
^^^^^^^^^^

To test a reusable Django app it's recommended to add a ``test_settings.py``
file to your app package to easily run the app tests with the ``test``
management command. Simply set the ``TEST_RUNNER`` setting to
``'discover_runner.DiscoverRunner'``, configure the other settings neccesary
to run your tests and call the ``test`` management command with the name of
the app package, e.g.:: 

    django-admin.py test --settings=myapp.test_settings myapp

Django project (Django >= 1.4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to test a project and want to store the project's tests outside
the project main package (recommended), you can simply follow the app
instructions above, applying it to the "project" package, but set a few
additional settings to tell the test runner to find the tests::

    from os import path
    TEST_DISCOVER_TOP_LEVEL = path.dirname(path.dirname(__file__))
    TEST_DISCOVER_ROOT = path.join(TEST_DISCOVER_TOP_LEVEL, 'tests')

This would find all the tests within a top-level "tests" package. Running the
tests is as easy as calling::

    django-admin.py test --settings=mysite.test_settings

Django project (Django < 1.4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the old project style you can simply leave out one call to the
``os.path.dirname`` function, since the old project directories were only
one level deep::

    from os import path
    TEST_DISCOVER_TOP_LEVEL = path.dirname(__file__)
    TEST_DISCOVER_ROOT = path.join(TEST_DISCOVER_TOP_LEVEL, 'tests')

Other than that it's similar to the new project's style configuration.

Thanks
------

This test runner is a humble rip-off of Carl Meyer's ``DiscoveryRunner``
which he published as a gist_ a while ago. All praise should be directed at
him. Thanks, Carl!

This is also very much related to ticket #17365_ and is hopefully useful
in replacing the default test runner in Django.

.. _unittest2: http://pypi.python.org/pypi/unittest2
.. _gist: https://gist.github.com/1450104
.. _#17365: https://code.djangoproject.com/ticket/17365

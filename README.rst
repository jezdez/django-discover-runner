django-discover-runner
======================

.. note::

    This runner has been added to Django 1.6 as the default test runner.
    If you use Django 1.6 or above you don't need this app.

An alternative Django ``TEST_RUNNER`` which uses the unittest2_ test discovery
from a base path specified in the settings, or any other module or package
specified to the ``test`` management command -- including app tests.

If you just run ``./manage.py test``, it'll discover and run all tests
underneath the current working directory. E.g. if you run
``./manage.py test full.dotted.path.to.test_module``, it'll run the tests in
that module (you can also pass multiple modules). If you give it a single
dotted path to a package (like a Django app) like ``./manage.py test myapp``
and that package does not itself directly contain any tests, it'll do
test discovery in all submodules of that package.

.. note::

    This code uses the default unittest2_ test discovery behavior, which
    only searches for tests in files named ``test*.py``. To override this
    see the ``TEST_DISCOVER_PATTERN`` setting or use the ``--pattern``
    option.

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

Installation
------------

Install it with your favorite installer, e.g.::

    pip install -U django-discover-runner

django-discover-runner requires at least Django 1.4 and also works on 1.5.x.
Starting in Django 1.6 the discover runner is a built-in.

Setup
-----

- ``TEST_RUNNER`` (required) needs to point to the ``DiscoverRunner`` class
  to enable it::

    TEST_RUNNER = 'discover_runner.DiscoverRunner'

- Add ``'discover_runner'`` to your ``INSTALLED_APPS`` setting to enable the
  ability to override the discovery settings below when using the ``test``
  management command.

- ``TEST_DISCOVER_TOP_LEVEL`` (optional) should be the directory containing
  your top-level package(s); in other words, the directory that should be on
  ``sys.path`` for your code to import. This is for example the directory
  containing ``manage.py`` in the new Django 1.4 project layout.
  The management command option is called ``--top-level``.

- ``TEST_DISCOVER_PATTERN`` (optional) is the pattern to use when discovering
  tests and defaults to the unittest2_ standard ``test*.py``. The management
  command option is called ``--pattern``.

Examples
--------

Django app
^^^^^^^^^^

To test a reusable Django app it's recommended to add a ``test_settings.py``
file to your app package to easily run the app tests with the ``test``
management command. Simply set the ``TEST_RUNNER`` setting to
``'discover_runner.DiscoverRunner'``, configure the other settings necessary
to run your tests and call the ``test`` management command with the name of
the app package, e.g.:: 

    django-admin.py test --settings=myapp.test_settings myapp

Django project
^^^^^^^^^^^^^^

If you want to test a project and want to store the project's tests outside
the project main package (recommended), you can simply follow the app
instructions above, applying it to the "project" package, but set a few
additional settings to tell the test runner to find the tests::

    from os import path
    TEST_DISCOVER_TOP_LEVEL = path.dirname(path.dirname(__file__))

This would find all the tests within a top-level "tests" package. Running the
tests is as easy as calling::

    django-admin.py test --settings=mysite.test_settings tests

Alternatively you can specify the ``--top-level-directory`` management
command option.

Multiple Django versions
^^^^^^^^^^^^^^^^^^^^^^^^

In case you want to test your app on older Django versions as well as
Django >= 1.6 you can simply conditionally configure the test runner in your
test settings, e.g.::

  import django

  if django.VERSION[:2] < (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'

Changelog
---------

1.0 06/15/2013
^^^^^^^^^^^^^^

* **GOOD NEWS!** This runner was added to Django 1.6 as the new default!
  This version backports that runner for Django 1.4.x and 1.5.x.

* Removed ``TEST_DISCOVER_ROOT`` setting in favor of unittest2's own way to
  figure out the root.

* Dropped support for Django 1.3.x.

0.4 04/12/2013
^^^^^^^^^^^^^^

* Added ability to override the discover settings with a custom test management
  command.

0.3 01/28/2013
^^^^^^^^^^^^^^

* Fixed setup.py to work on Python 3. This should make this app compatible
  to Python 3.

0.2.2 09/04/2012
^^^^^^^^^^^^^^^^

* Stopped setting the top level variable in the case of using a module path
  as the test label as it made the wrong assumption that the parent directory
  *is* the top level.

0.2.1 08/20/2012
^^^^^^^^^^^^^^^^

* Fixed a rather esoteric bug with testing test case class methods
  that was caused by a wrong import and the way Django wraps itself
  around the unittest2 module (if availale) or unittest on Python >= 2.7.

0.2 05/26/2012
^^^^^^^^^^^^^^

* Added ability to use an optionally installed unittest2 library
  for Django projects using Django < 1.3 (which added unittest2 to the
  ``django.utils.unittest`` package).

0.1.1 05/23/2012
^^^^^^^^^^^^^^^^

* Fixed a bug that prevented the project based feature to work correctly.

0.1 05/20/2012
^^^^^^^^^^^^^^

* Initial release with support for Django >= 1.3.

Thanks
------

This test runner is a humble rip-off of Carl Meyer's ``DiscoveryRunner``
which he published as a gist_ a while ago. All praise should be directed at
him. Thanks, Carl!

This was also very much related to ticket `#17365`_ which eventually led
to the replacement of the default test runner in Django. Thanks **again**,
Carl!

.. _unittest2: http://pypi.python.org/pypi/unittest2
.. _gist: https://gist.github.com/1450104
.. _`#17365`: https://code.djangoproject.com/ticket/17365

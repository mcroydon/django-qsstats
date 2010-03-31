==============================================
django-qsstats: QuerySet statistics for Django
==============================================

The goal of django-qsstats is to be a microframework to make
repetitive tasks such as generating aggregate statistics of querysets
over time easier.  It's probably overkill for the task at hand, but yay
microframeworks!

Requirements
============

* `python-dateutil <http://labix.org/python-dateutil>`_
* `django <http://www.djangoproject.com/>`_ 1.1+

License
=======

Liensed under a BSD-style license.

Examples
========

How many users signed up today? this month? this year?
------------------------------------------------------

::

    from django.contrib.auth import User
    import qsstats
    
    qs = User.objects.all()
    qss = qsstats.QuerySetStats(qs, 'date_joined')
    
    print '%s new accounts today.' % qss.this_day()
    print '%s new accounts this month.' % qss.this_month()
    print '%s new accounts this year.' % qss.this_year()
    print '%s new accounts until now.' % qss.until_now()

This might print something like::

    5 new accounts today.
    27 new accounts this month.
    377 new accounts this year.
    409 new accounts until now.

Aggregating time-series data suitable for graphing
--------------------------------------------------

::

    from django.contrib.auth import User
    import datetime, qsstats

    qs = User.objects.all()
    qss = qsstats.QuerySetStats(qs, 'date_joined')
    
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)

    time_series = qss.time_series(seven_days_ago, today)
    print 'New users in the last 7 days: %s' % [t[1] for t in time_series]

This might print something like::

    New users in the last 7 days: [3, 10, 7, 4, 12, 9, 11]

Please see qsstats/tests.py for similar usage examples.

API
===

The ``QuerySetStats`` object
----------------------------

In order to provide maximum flexibility, the ``QuerySetStats`` object
can be instantiated with as little or as much information as you like.
All keword arguments are optional but ``DateFieldMissing`` and
``QuerySetMissing`` will be raised if you try to use ``QuerySetStats``
without providing enough information.

``qs``
    The queryset to operate on.
    
    Default: ``None``

``date_field``
    The date field within the queryset to use.

    Default: ``None``

``aggregate_field``
    The field to use for aggregate data.  Can be set system-wide with
    the setting ``QUERYSETSTATS_DEFAULT_AGGREGATE_FIELD`` or set when
    instantiating or calling one of the methods.
    
    Default: ``'id'``

``aggregate_class``
    The aggregate class to be called during aggregation operations.  Can
    be set system-wide with the setting ``QUERYSETSTATS_DEFAULT_AGGREGATE_CLASS``
    or set when instantiating or calling one of the methods.

    Default: ``Count``

``operator``
    The default operator to use for the ``pivot`` function.  Can be set
    system-wide with the setting ``QUERYSETSTATS_DEFAULT_OPERATOR`` or
    set when calling ``pivot``.
    
    Default: ``'lte'``


All of the documented methods take a standard set of keyword arguments that override any information already stored within the ``QuerySetStats`` object.  These keyword arguments are ``date_field``, ``aggregate_field``, ``aggregate_class``.

Once you have a ``QuerySetStats`` object instantiated, you can receive a single aggregate result by using the following methods:

``for_day``
    Positional arguments: ``dt``, a ``datetime.datetime`` or ``datetime.date`` object
    to filter the queryset to this day.

``this_day``
    A wrapper around ``for_day`` that provides aggregate information for ``datetime.date.today()``.  It takes no positional arguments.

``for_month``
    Positional arguments: ``dt``, a ``datetime.datetime`` or ``datetime.date`` object to filter the queryset to this month.

``this_month``
    A wrapper around ``for_month`` that uses ``dateutil.relativedelta`` to provide aggregate information for this current month.

``for_year``
    Positional arguments: ``dt``, a ``datetime.datetime`` or ``datetime.date`` object to filter the queryset to this year.

``this_year``
    A wrapper around ``for_year`` that uses ``dateutil.relativedelta`` to provide aggregate information for this current year.

``QuerySetStats`` also provides a method for returning aggregated
time-series data which may be extremely using in plotting data:

``time_series``
    Positional arguments: ``start_date`` and ``end_date``, each a ``datetime.date`` or ``datetime.datetime`` object used in marking the start and stop of the time series data.

    Keyword arguments: In addition to the standard ``date_field``,
    ``aggregate_field``, and ``aggregate_class`` keyword argument,
    ``time_series`` takes an optional ``interval`` keyword argument
    used to mark which interval to use while calculating aggregate
    data between ``start_date`` and ``end_date``.  This argument
    defaults to ``'days'`` and can accept ``'years'``, ``'months'``,
    ``'weeks'``, or ``'days'``.  It will raise ``InvalidInterval``
    otherwise.

    This methods returns a list of tuples.  The first item in each
    tuple is a ``datetime.date`` object for the current inverval.  The
    second item is the result of the aggregate operation.  For
    example::

        [(datetime.date(2010, 3, 28), 12), (datetime.date(2010, 3, 29), 0), ...]

    Formatting of date information is left as an exercise to the user and may
    vary depending on interval used.

``until``
    Provide aggregate information until a given date or time, filtering the
    queryset using ``lte``.
    
    Positional arguments: ``dt`` a ``datetime.date`` or ``datetime.datetime``
    object to be used for filtering the queryset since.

    Keyword arguments: ``date_field``, ``aggregate_field``, ``aggregate_class``.

``until_now``
    Aggregate information until now.

    Positional arguments: ``dt`` a ``datetime.date`` or ``datetime.datetime``
    object to be used for filtering the queryset since (using ``lte``).

    Keyword arguments: ``date_field``, ``aggregate_field``, ``aggregate_class``.

``after``
    Aggregate information after a given date or time, filtering the queryset
    using ``gte``.
    
    Positional arguments: ``dt`` a ``datetime.date`` or ``datetime.datetime``
    object to be used for filtering the queryset since.
    
    Keyword arguments: ``date_field``, ``aggregate_field``, ``aggregate_class``.

``after_now``
    Aggregate information after now.

    Positional arguments: ``dt`` a ``datetime.date`` or ``datetime.datetime``
    object to be used for filtering the queryset since (using ``gte``).

    Keyword arguments: ``date_field``, ``aggregate_field``, ``aggregate_class``.

``pivot``
    Used by ``since``, ``after``, and ``until_now`` but potentially useful if
    you would like to specify your own operator instead of the defaults.

    Positional arguments: ``dt`` a ``datetime.date`` or ``datetime.datetime``
    object to be used for filtering the queryset since (using ``lte``).

    Keyword arguments: ``operator``, ``date_field``, ``aggregate_field``, ``aggregate_class``.
    
    Raises ``InvalidOperator`` if the operator provided is not one of ``'lt'``,
    ``'lte'``, ``gt`` or ``gte``.

Testing
=======

If you'd like to test ``django-qsstats`` against your local configuration, add
``qsstats`` to your ``INSTALLED_APPS`` and run ``./manage.py test qsstats``.  The test suite assumes that ``django.contrib.auth`` is installed.

TODO
====

* There's a bunch of boilerplate that I'm sure could be reduced.
* Clearer documentation and usage examples.
* More test coverage.

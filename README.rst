==============================================
django-qsstats: QuerySet statistics for Django
==============================================

The goal of django-qsstats is to be a microframework to make
repetitive tasks such as generating aggregate statistics of querysets
over time easier.

Examples
========

How many users signed up today? this month? this year?
------------------------------------------------------

::

    from django.contrib.auth import User
    import qsstats
    
    qs = User.objects.all()
    qss = qsstats.QuerySetStats(qs, 'date-joined')
    
    print '%s new accounts today.' % qss.this_day()
    print '%s new accounts this month.' % qss.this_month()
    print '%s new accounts this year.' % qss.this_year()

This might print something like::

    5 new accounts today.
    27 new accounts this month.
    377 new accounts this year.

Aggregating time-series data suitable for graphing
--------------------------------------------------

::

    from django.contrib.auth import User
    import datetime, qsstats

    qs = User.objects.all()
    qss = qsstats.QuerySetStats(qs, 'date-joined')
    
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)

    time_series = qss.time_series(seven_days_ago, today)
    print 'New users in the last 7 days: %s' % [t[1] for t in time_series]

This might print something like::

    New users in the last 7 days: [3, 10, 7, 4, 12, 9, 11]

Requirements
============

* `python-dateutil <http://labix.org/python-dateutil>`_
* `django <http://www.djangoproject.com/>`_ 1.1+

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

Requirements
============

* `python-dateutil <http://labix.org/python-dateutil>`_
* `django <http://www.djangoproject.com/>`_ 1.1+

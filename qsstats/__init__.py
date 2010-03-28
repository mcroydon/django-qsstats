from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db.models import Count
import datetime

class InvalidInterval(Exception):
    pass

class DateFieldMissing(Exception):
    pass

class QuerySetMissing(Exception):
    pass

class QuerySetStats(object):
    """
    Generates statistics about a queryset using Django aggregates.  QuerySetStats
    is able to handle snapshots of data (for example this day, week, month, or
    year) or generate time series data suitable for graphing.
    """
    def __init__(self, qs=None, date_field=None, aggregate=None):
        self.qs = qs
        self.date_field = date_field
        self.aggregate = aggregate or getattr(settings, 'QUERYSETSTATUS_DEFAULT_AGGREGATE', Count)
        # MC_TODO: Danger in caching this?
        self.update_today()

    # Aggregates for a specific period of time

    def for_day(self, dt, date_field=None, aggregate=None):
        date_field = date_field or self.date_field
        aggregate = aggregate or self.aggregate
        self.check_date_field(date_field)
        self.check_qs()

        kwargs = {
            '%s__year' % date_field : dt.year,
            '%s__month' % date_field : dt.month,
            '%s__day' % date_field : dt.day,
        }
        agg = self.qs.filter(**kwargs).aggregate(agg=aggregate('id'))
        return agg['agg']

    def this_day(self, date_field=None, aggregate=None):
        date_field = date_field or self.date_field
        aggregate = aggregate or self.aggregate

        return self.for_day(self.today, date_field, aggregate)

    def for_month(self, dt, date_field=None, aggregate=None):
        date_field = date_field or self.date_field
        aggregate = aggregate or self.aggregate
        self.check_date_field(date_field)
        self.check_qs()

        first_day = datetime.date(year=dt.year, month=dt.month, day=1)
        last_day = first_day + relativedelta(day=31)
        return self.get_aggregate(first_day, last_day, date_field, aggregate)

    def this_month(self, date_field=None, aggregate=None):
        date_field = date_field or self.date_field
        aggregate = aggregate or self.aggregate

        return self.for_month(self.today, date_field, aggregate)

    def for_year(self, dt, date_field=None, aggregate=None):
        date_field = date_field or self.date_field
        aggregate = aggregate or self.aggregate
        self.check_date_field(date_field)
        self.check_qs()

        first_day = datetime.date(year=dt.year, month=1, day=1)
        last_day = datetime.date(year=dt.year, month=12, day=31)
        return self.get_aggregate(first_day, last_day, date_field, aggregate)

    def this_year(self, date_field=None, aggregate=None):
        date_field = date_field or self.date_field
        aggregate = aggregate or self.aggregate

        return self.for_year(self.today, date_field, aggregate)

    # Aggregate over time intervals

    def time_series(self, start_date, end_date, interval='days', date_field=None, aggregate=None):
        if interval not in ('years', 'months', 'weeks', 'days'):
            raise InvalidInterval('Inverval not supported.')

        date_field = date_field or self.date_field
        aggregate = aggregate or self.aggregate

        self.check_date_field(date_field)
        self.check_qs()

        stat_list = []
        dt = start_date
        while dt < end_date:
            # MC_TODO: Less hacky way of doing this?
            method = getattr(self, 'for_%s' % interval.rstrip('s'))
            stat_list.append((dt, method(dt, date_field=date_field, aggregate=aggregate)))
            dt = dt + relativedelta(**{interval : 1})
        return stat_list

    # Utility functions
    def update_today(self):
        self.today = datetime.date.today()

    def get_aggregate(self, first_day, last_day, date_field, aggregate):
        # MC_TODO: Allow aggregate field to be passed down
        #          instead of hard-coding id.
        kwargs = {'%s__range' % date_field : (first_day, last_day)}
        agg = self.qs.filter(**kwargs).aggregate(agg=aggregate('id'))
        return agg['agg']

    def check_date_field(self, date_field):
        if not date_field:
            raise DateFieldMissing("Please provide a date_field.")

    def check_qs(self):
        if not self.qs:
            raise QuerySetMissing("Please provide a queryset.")

if __name__ == '__main__':
    """
    This generates:
    x new accounts this month.
    y new accounts this year.
    """
    # User example
    from django.contrib.auth.models import User
    qs = User.objects.all()
    qss = QuerySetStats(qs, 'date_joined')
    print "%s new accounts this month." % qss.this_month()
    print "%s new accounts this year." % qss.this_year()
    today = datetime.date.today()
    earlier = today - relativedelta(days=10)
    print "Stats for the last few days: %s" % qss.time_series(earlier, today)

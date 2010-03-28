from dateutil.relativedelta import relativedelta
from django.db.models import Count
import datetime

class QuerySetStats(object):
    """
    Generates statistics for a queryset.
    """
    def __init__(self, qs, date_field=None):
        self.qs = qs
        self.date_field = date_field
        # MC_TODO: Danger in caching this?
        self.update_today()

    # MC_TODO: investigate dynamic dispatch?

    def for_day(self, dt, date_field=None, aggregate=Count):
        date_field = date_field or self.date_field
        kwargs = {
            '%s__year' % date_field : dt.year,
            '%s__month' % date_field : dt.month,
            '%s__day' % date_field : dt.day,
        }
        agg = self.qs.filter(**kwargs).aggregate(agg=aggregate('id'))
        return agg['agg']

    def this_day(self, date_field=None, aggregate=Count):
        date_field = date_field or self.date_field
        return self.for_day(self.today, date_field, aggregate)

    def for_month(self, dt, date_field=None, aggregate=Count):
        date_field = date_field or self.date_field

        first_day = datetime.date(year=dt.year, month=dt.month, day=1)
        last_day = first_day + relativedelta(day=31)
        return self.get_aggregate(first_day, last_day, date_field, aggregate)

    def this_month(self, date_field=None, aggregate=Count):
        return self.for_month(self.today, date_field, aggregate)

    def for_year(self, dt, date_field=None, aggregate=Count):
        date_field = date_field or self.date_field
 
        first_day = datetime.date(year=dt.year, month=1, day=1)
        last_day = datetime.date(year=dt.year, month=12, day=31)
        return self.get_aggregate(first_day, last_day, date_field, aggregate)

    def this_year(self, date_field=None, aggregate=Count):
        return self.for_year(self.today, date_field, aggregate)

    # Utility functions
    def update_today(self):
        self.today = datetime.date.today()

    def get_aggregate(self, first_day, last_day, date_field, aggregate):
        kwargs = {'%s__range' % date_field : (first_day, last_day)}
        agg = self.qs.filter(**kwargs).aggregate(agg=aggregate('id'))
        return agg['agg']

        

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

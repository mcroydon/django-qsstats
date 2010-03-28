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

    def this_month(self, date_field=None):
        date_field = date_field or self.date_field

        first_day = datetime.date(year=self.today.year, month=self.today.month, day=1)
        last_day = first_day + relativedelta(day=31)
        return self.get_count(first_day, last_day, date_field)

    def this_year(self, date_field=None):
        date_field = date_field or self.date_field
        first_day = datetime.date(year=self.today.year, month=1, day=1)
        last_day = datetime.date(year=self.today.year, month=12, day=31)
        return self.get_count(first_day, last_day, date_field)

    # Utility functions
    def update_today(self):
        self.today = datetime.date.today()

    def get_count(self, first_day, last_day, date_field):
        kwargs = {'%s__range' % date_field : (first_day, last_day)}
        agg = qs.filter(**kwargs).aggregate(count=Count('id'))
        return agg['count']
        

if __name__ == '__main__':
    """
    This generates:
    15 new accounts this month
    104 new accounts this year
    """
    # User example
    from django.contrib.auth.models import User
    qs = User.objects.all()
    qss = QuerySetStats(qs, 'date_joined')
    print "%s new accounts this month." % qss.this_month()
    print "%s new accounts this year." % qss.this_year()


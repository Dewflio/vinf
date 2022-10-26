import datetime

class DateBC(datetime.datetime):
    bc = False
    year_active = False
    month_active = False
    day_active = False
    def __str__(self):
        prefix = '-' if self.bc else ''
        return u'%s%s' % (prefix, super(DateBC, self).__str__(),)
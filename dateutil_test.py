import dateutil.parser
import datetime

old_init = dateutil.parser._parser._ymd.__init__
def new_init(self, *args, **kwargs):
    old_init(self, *args, **kwargs)
    self.century_specified = True

dateutil.parser._parser._ymd.__init__ = new_init
print(dateutil.parser.parse('01 01 0003'))


a = datetime.datetime(3, 1,1)
print(a)

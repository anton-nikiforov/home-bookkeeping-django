from collections import OrderedDict

import six, hashlib
from funcy import memoize

# Adapt hashlib.md5 to eat str in python 3
if six.PY2:
    md5 = hashlib.md5
else:
    class md5:
        def __init__(self, s=None):
            self.md5 = hashlib.md5()
            if s is not None:
                self.update(s)

        def update(self, s):
            return self.md5.update(s.encode('utf-8'))

        def hexdigest(self):
            return self.md5.hexdigest()

def md5hex(s):
    return md5(s).hexdigest()

@memoize
def stamp_fields(model):
    """
    Returns serialized description of model fields.
    """
    stamp = str([(f.name, f.attname, f.db_column, f.__class__) for f in model._meta.fields])
    return md5hex(stamp)    

def reorder_fields(fields, order):
    """Reorder form fields by order, removing items not in order.

    >>> reorder_fields(
    ...     OrderedDict([('a', 1), ('b', 2), ('c', 3)]),
    ...     ['b', 'c', 'a'])
    OrderedDict([('b', 2), ('c', 3), ('a', 1)])
    """
    for key, v in fields.items():
        if key not in order:
            del fields[key]

    return OrderedDict(sorted(fields.items(), key=lambda k: order.index(k[0])))
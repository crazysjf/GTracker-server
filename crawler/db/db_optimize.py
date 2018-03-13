# -*- coding: utf-8 -*-

from db import DB
from csv_processor import import_files_in_dir, import_to_db
from datetime import datetime

t1 = datetime.now()
#import_to_db('110471204', date(2018, 1, 27), f)
import_files_in_dir('../network/csv/', 'data.db')
t2 = datetime.now()
print t2 - t1
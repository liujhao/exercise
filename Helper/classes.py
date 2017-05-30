#/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import datetime

#
class CJsonEncoder(json.JSONEncoder):
    '''
    DjangoSet列表中的字段类型自定义转换
    '''
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
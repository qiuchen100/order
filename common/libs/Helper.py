# -*- coding: utf-8 -*-
from flask import g, render_template
import math


def ops_render(template, context = {}):
    '''
    统一渲染方法
    '''
    if 'current_user' in g:
        context['current_user'] = g.current_user

    return render_template(template, **context)


def iPagination( params ):
    '''
    自定义分页类
    '''
    ret = {
        "is_prev":1,
        "is_next":1,
        "from" :0 ,
        "end":0,
        "current":0,
        "total_pages":0,
        "page_size" : 0,
        "total" : 0,
        "url":params['url'].replace("&p=","")
    }

    total = int( params['total'] )
    page_size = int( params['page_size'] )
    page = int( params['page'] )
    display = int( params['display'] )
    total_pages = int( math.ceil( total / page_size ) )
    total_pages = total_pages if total_pages > 0 else 1

    if page <= 1:
        ret['is_prev'] = 0

    if page >= total_pages:
        ret['is_next'] = 0

    semi = int( math.ceil( display / 2 ) )

    ret['from'] = page - semi if page - semi > 0 else 1
    ret['end'] = page + semi if page + semi <= total_pages else total_pages
    ret['current'] = page
    ret['total_pages'] = total_pages
    ret['page_size'] = page_size
    ret['total'] = total
    ret['range'] = range( ret['from'],ret['end'] + 1 )
    return ret

#This file is part nereid_cms module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.pool import Pool
from .cms import *
from .routing import *

def register():
    Pool.register(
        Menu,
        Article,
        Banner,
        WebSite,
        module='nereid_cms', type_='model')

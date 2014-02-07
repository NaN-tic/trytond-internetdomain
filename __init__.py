#This file is part internetdomain module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.pool import Pool
from .company import *
from .internetdomain import *


def register():
    Pool.register(
        Company,
        Domain,
        Renewal,
        DomainProduct,
        module='internetdomain', type_='model')

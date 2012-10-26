#This file is part internetdomain module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta

__all__ = ['Company']
__metaclass__ = PoolMeta

class Company:
    'Company'
    __name__ = 'company.company'
    
    idomain_alert_expire = fields.Char('Domain Alert Expire',
        help='Days notice of expire (separated with comma. Ex. 30,15,10)')


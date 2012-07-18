#This file is part internetdomain module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields

class Company(ModelSQL, ModelView):
    'Company'
    _name = 'company.company'
    _description = __doc__
    
    idomain_alert_expire = fields.Char('Domain Alert Expire', help='Days notice of expire (separated with comma. Ex. 30,15,10)')

Company()

#This file is part internetdomain module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields
from trytond.tools import safe_eval, datetime_strftime
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.pyson import If, Eval, Bool

import datetime

class Domain(ModelSQL, ModelView):
    'Domain'
    _name = 'internetdomain.domain'
    _description = __doc__

    company = fields.Many2One('company.company', 'Company', required=True,
        domain=[
            ('id', If(Eval('context', {}).contains('company'), '=', '!='),
                Eval('context', {}).get('company', 0)),
            ])
    name = fields.Char('Name', required=True)
    date_create = fields.Date('Date Create', 
        required=True)
    date_expire = fields.Function(fields.Date('Date expired'),
        'get_expire')
    warning = fields.Function(fields.Boolean('Warning expired'),
        'get_warning')
    party = fields.Many2One('party.party', 'Party', 
        on_change=['party', 'party_address', 'company'], required=True)
    party_address = fields.Many2One('party.address', 'Address',
        required=True, depends=['party'],
        domain=[('party', '=', Eval('party'))])
    registrator = fields.Function(fields.Many2One('party.party', 'Registrator'),
        'get_registrator')
    registrator_website = fields.Function( fields.Char('Website'),
        'get_registrator_website')
    dns1 = fields.Char('DNS Primary')
    dns2 = fields.Char('DNS Secundary')
    dns3 = fields.Char('DNS Secundary (2)')
    dns4 = fields.Char('DNS Secundary (3)')
    ip = fields.Char('IP')
    comment = fields.Text('Comment')
    active = fields.Boolean('Active')
    renewal = fields.One2Many('internetdomain.renewal', 'domain', 'Renewals',
        order=[('date_renewal', 'DESC')])
    products = fields.Many2Many('internetdomain.domain-domain.product',
        'domain', 'product', 'Products')

    def default_active(self):
        return True

    def default_company(self):
        return Transaction().context.get('company')

    def get_last_renewal(self, domain):
        """Get last renewal from fomain
        :param domain: Domain object
        :return: ID or False
        """

        renewal = False
        renewal_obj = Pool().get('internetdomain.renewal')
        renewals = renewal_obj.search(
            [('domain', '=', domain.id)],
            order=[('date_renewal', 'DESC')]
            )
        if len(renewals)>0:
            renewal = renewal_obj.browse(renewals[0])
        return renewal

    def get_registrator(self, ids, name):
        """Get registrator from domain"""
        result = {}
        for domain in self.browse(ids):
            renewal = self.get_last_renewal(domain)
            result[domain.id] = renewal and renewal.registrator.id or False
        return result

    def get_registrator_website(self, ids, name):
        """Get registrator website from domain"""
        result = {}
        for domain in self.browse(ids):
            renewal = self.get_last_renewal(domain)
            result[domain.id] = renewal and renewal.registrator.website or False
        return result

    def get_expire(self, ids, name):
        """Get expire date from domain"""
        result = {}
        for domain in self.browse(ids):
            renewal = self.get_last_renewal(domain)
            result[domain.id] = renewal and renewal.date_expire or False
        return result

    def get_warning(self, ids, name):
        """Get warning if last registration pass today"""
        result = {}
        for domain in self.browse(ids):
            warning_expire = False
            renewal = self.get_last_renewal(domain)

            if not domain.company.idomain_alert_expire:
                max_alert = 30 #30 days
            else:
                intdomain_alert_expire = domain.company.idomain_alert_expire.split(',')
                intdomain_alert_expire = [int(x) for x in intdomain_alert_expire]
                max_alert = intdomain_alert_expire[0]
                for x in intdomain_alert_expire:
                    if x > max_alert:
                        max_alert = x

            if domain.date_expire:
                today = datetime.date.today()
                date_exp = domain.date_expire
                diff_date = datetime.timedelta()
                diff_date = date_exp - today
                if diff_date.days <= max_alert:
                    warning_expire = True

            result[domain.id] = warning_expire

        return result

    def on_change_party(self, vals):
        pool = Pool()
        party_obj = pool.get('party.party')
        address_obj = pool.get('party.address')
        res = {
            'party_address': None,
        }

        if vals.get('party'):
            party = party_obj.browse(vals['party'])
            res['party_address'] = party_obj.address_get(party.id,
                    type='invoice')
        if res['party_address']:
            res['party_address.rec_name'] = address_obj.browse(
                    res['party_address']).rec_name
        return res

    def on_change_registrator(self, values):
        """When change registrator, get website value"""
        party_obj = Pool().get('party.party')
        registrator = values.get('registrator', False)
        res['registrator_website'] = None
        if registrator:
            party = party_obj.browse(registrator)
            res['registrator_website'] = party.website and \
                    party.website or None
        return res

Domain()

class Renewal(ModelSQL, ModelView):
    'Renewal'
    _name = 'internetdomain.renewal'
    _description = __doc__

    domain = fields.Many2One('internetdomain.domain', 'Domain', 
        ondelete='CASCADE', select=True)
    date_renewal = fields.Date('Date Renewal', required=True)
    date_expire = fields.Date('Date Expire', required=True)
    registrator = fields.Many2One('party.party', 'Registrator', required=True)
    comment = fields.Text('Comment')

Renewal()

class DomainProduct(ModelSQL):
    'Domain - Product'
    _name = 'internetdomain.domain-domain.product'
    _table = 'internetdomain_domain_product_rel'
    _description = __doc__

    domain = fields.Many2One('internetdomain.domain', 'Domain', ondelete='CASCADE',
            required=True, select=True)
    product = fields.Many2One('product.product', 'Product',
        ondelete='CASCADE', required=True, select=True)

DomainProduct()

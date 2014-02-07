#This file is part internetdomain module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.pyson import If, Eval

import datetime

__all__ = ['Domain', 'Renewal', 'DomainProduct']

class Domain(ModelSQL, ModelView):
    'Domain'
    __name__ = 'internetdomain.domain'

    company = fields.Many2One('company.company', 'Company', required=True,
        domain=[
            ('id', If(Eval('context', {}).contains('company'), '=', '!='),
                Eval('context', {}).get('company', 0)),
            ])
    name = fields.Char('Name', required=True)
    date_create = fields.Date('Date Create', 
        required=True)
    date_expire = fields.Function(fields.Date('Date expired'),
        'get_expire', searcher='search_expire')
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

    @staticmethod
    def default_active():
        return True

    @staticmethod
    def default_company():
        return Transaction().context.get('company')

    def get_last_renewal(self):
        """Get last renewal from domain"""
        renewal = False
        Renewal = Pool().get('internetdomain.renewal')
        renewals = Renewal.search(
            [('domain', '=', self.id)],
            order=[('date_renewal', 'DESC')]
            )
        if len(renewals)>0:
            renewal = Renewal(renewals[0].id)
        return renewal

    def get_registrator(self, name=None):
        """Get registrator from domain"""
        renewal = self.get_last_renewal()
        return renewal and renewal.registrator.id or None

    def get_registrator_website(self, name=None):
        """Get registrator website from domain"""
        renewal = self.get_last_renewal()
        return renewal and renewal.registrator.website or None

    def get_expire(self, name=None):
        """Get expire date from domain"""
        renewal = self.get_last_renewal()
        return renewal and renewal.date_expire or None

    @classmethod
    def search_expire(cls, name, clause):
        return [('renewal.date_expire',) + tuple(clause[1:])]

    @classmethod
    def get_warning(cls, records, name):
        """Get warning if last registration pass today"""
        result = {}
        for domain in records:
            warning_expire = False

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

    def on_change_party(self):
        address = None
        changes = {}
        if self.party:
            address = self.party.address_get()
        if address:
            changes['party_address'] = address.id
        return changes

    def on_change_registrator(self):
        """When change registrator, get website value"""
        Party = Pool().get('party.party')

        changes = {}
        changes['registrator_website'] = None
        if self.registrator:
            party = Party.browse([self.registrator])[0]
            changes['registrator_website'] = party.website and \
                    party.website or None
        return changes


class Renewal(ModelSQL, ModelView):
    'Renewal'
    __name__ = 'internetdomain.renewal'

    domain = fields.Many2One('internetdomain.domain', 'Domain', 
        ondelete='CASCADE', select=True, required=True)
    date_renewal = fields.Date('Date Renewal', required=True)
    date_expire = fields.Date('Date Expire', required=True)
    registrator = fields.Many2One('party.party', 'Registrator', required=True)
    comment = fields.Text('Comment')


class DomainProduct(ModelSQL):
    'Domain - Product'
    __name__ = 'internetdomain.domain-domain.product'
    _table = 'internetdomain_domain_product_rel'

    domain = fields.Many2One('internetdomain.domain', 'Domain', ondelete='CASCADE',
            required=True, select=True)
    product = fields.Many2One('product.product', 'Product',
        ondelete='CASCADE', required=True, select=True)


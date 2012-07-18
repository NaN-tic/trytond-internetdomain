#!/usr/bin/env python
#This file is part internetdomain module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

import sys
import os
DIR = os.path.abspath(os.path.normpath(os.path.join(__file__,
    '..', '..', '..', '..', '..', 'trytond')))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))

import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT, test_view,\
    test_depends
from trytond.transaction import Transaction

import datetime

class DomainTestCase(unittest.TestCase):
    '''
    Test Internet Domain module.
    '''

    def setUp(self):
        trytond.tests.test_tryton.install_module('internetdomain')
        self.currency = POOL.get('currency.currency')
        self.domain = POOL.get('internetdomain.domain')
        self.renewal = POOL.get('internetdomain.renewal')
        self.company = POOL.get('company.company')
        self.party = POOL.get('party.party')
        self.address = POOL.get('party.address')
        self.user = POOL.get('res.user')

    def test0005views(self):
        '''
        Test views.
        '''
        test_view('internetdomain')

    def test0006depends(self):
        '''
        Test depends.
        '''
        test_depends()

    def test0010domain(self):
        '''
        Create domains
        '''

        with Transaction().start(DB_NAME, USER,
                context=CONTEXT) as transaction:
            currency_id = self.currency.create({
                'name': 'cu1',
                'symbol': 'cu1',
                'code': 'cu1'
                })
            company_id = self.company.create({
                'name': 'Zikzakmedia',
                'currency': currency_id,
                })
            self.user.write(USER, {
                'main_company': company_id,
                'company': company_id,
                })
            party_id = self.party.create({
                'name': 'Zikzakmedia',
                'code': '001',
                })
            address_id = self.address.create({
                'name': 'Raimon Esteve',
                'party': party_id,
                })
            domain_id = self.domain.create({
                'name': 'zikzakmedia.com',
                'date_create': datetime.date(2011, 10, 1),
                'party': party_id,
                'party_address': address_id,
                'company': company_id,
                })
            renewal_id = self.renewal.create({
                'domain': domain_id,
                'date_renewal': '2012-06-01',
                'date_expire': '2013-06-01',
                'registrator': company_id,
                })
            self.assert_(domain_id)

            transaction.cursor.commit()

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        DomainTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

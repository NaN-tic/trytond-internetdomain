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
        '''Create domain'''
        with Transaction().start(DB_NAME, USER, context=CONTEXT) as transaction:
            company, = self.company.search([('rec_name', '=', 'Dunder Mifflin')])
            self.user.write([self.user(USER)], {
                    'main_company': company.id,
                    'company': company.id,
                    })
            CONTEXT.update(self.user.get_preferences(context_only=True))
            party, = self.party.create([{
                'name': 'Zikzakmedia',
                'code': '001',
                }])
            address, = self.address.create([{
                'name': 'Raimon Esteve',
                'party': party.id,
                }])
            domain, = self.domain.create([{
                'name': 'zikzakmedia.com',
                'date_create': datetime.date(2011, 10, 1),
                'party': party.id,
                'party_address': address.id,
                'company': company.id,
                }])
            self.renewal.create([{
                'domain': domain.id,
                'date_renewal': '2012-06-01',
                'date_expire': '2013-06-01',
                'registrator': company.id,
                }])
            self.assert_(domain.id)

            transaction.cursor.commit()

def suite():
    suite = trytond.tests.test_tryton.suite()
    from trytond.modules.company.tests import test_company
    for test in test_company.suite():
        if test not in suite:
            suite.addTest(test)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        DomainTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

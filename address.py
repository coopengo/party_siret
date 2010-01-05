#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import Model, fields
import luhn


class Address(Model):
    _name = 'party.address'

    siret_nic = fields.Char('SIRET NIC', select=1, states={
        'readonly': "active == False",
        }, size=5)
    siret = fields.Function('get_siret', type='char', string='SIRET')

    def __init__(self):
        super(Address, self).__init__()
        self._constraints += [
            ('check_siret', 'invalid_siret'),
        ]
        self._error_messages.update({
            'invalid_siret': 'Invalid SIRET number!',
        })

    def get_siret(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for address in self.browse(cursor, user, ids, context=context):
            if address.party.siren and address.siret_nic:
                res[address.id] = address.party.siren + address.siret_nic
            else:
                res[address.id] = ''
        return res

    def check_siret(self, cursor, user, ids):
        '''
        Check validity of SIRET
        '''
        for address in self.browse(cursor, user, ids):
            if address.siret and not luhn.validate(address.siret):
                return False
        return True

Address()

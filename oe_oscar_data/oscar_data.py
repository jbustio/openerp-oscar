# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010, 2014 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import requests
import simplejson
from openerp import models, fields
from openerp.tools import config
from openerp.addons.oe_oscar_data.csv_utils import CsvUnicodeReader

class OscarData(models.Model):
    _name = 'oscar.data'

    name = fields.Char('Model Name', size=128, required=1)
    filepath = fields.Char('Dir file', size=128)
    
    def import_data(self, cr, uid, ids, context= None):
        obj = self.browse(cr, uid, ids[0])
        file_path = obj.filepath
        
        print file_path
        delimiter = '@'
        market_price = self.pool.get('market.price.by.date')
        row_number = 0
        for row in CsvUnicodeReader(open(file_path, 'rb'),
                                    delimiter=delimiter, quotechar='"',
                                    escapechar='\\'):
            row_number += 1
            vals = {}
            if row_number > 1:
                vals['markettype'] = row[0]
                vals['commodityname'] = row[1]
                vals['cityname'] = row[2]
                vals['variety'] = row[3]
                vals['color'] = row[4]
                vals['origin'] = row[5]
                vals['date'] = row[6]
                vals['per_lb'] = row[7]
                market_price.create(cr,uid,vals,context)
                
                
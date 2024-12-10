# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    procedure_ids = fields.Many2many('medical.procedure', string='Procedures')
    ensurance_id = fields.Many2one('medical.ensurance', string='Ensurance')

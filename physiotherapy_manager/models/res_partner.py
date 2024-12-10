# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ensurance_id = fields.Many2one('medical.ensurance', string='Ensurance')
    contact_type = fields.Selection(
        [('patient', 'Patient'), ('medic', 'Medic'), ('therapist', 'Therapist')], string='Type')
    age = fields.Integer(string='Age')

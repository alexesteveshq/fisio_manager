# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ensurance_id = fields.Many2one('medical.ensurance', string='Ensurance')
    contact_type = fields.Selection(
        [('patient', 'Patient'), ('medic', 'Medic'), ('therapist', 'Therapist')], string='Type')
    age = fields.Integer(string='Age')
    color = fields.Integer(string='Color')

    @api.constrains('vat')
    def _check_vat(self):
        for partner in self:
            partners = self.env['res.partner'].search([('vat', '=', partner.vat)])
            if partners:
                raise ValidationError(_('There is already a contact created with the same VAT.'))

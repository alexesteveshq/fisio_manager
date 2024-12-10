# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class MedicalEvolution(models.Model):
    _name = 'medical.evolution'
    _description = 'Medical Evolution'

    name = fields.Char(string='Name')
    date = fields.Date(string='Date')
    description = fields.Text(string='Description')
    consultation_id = fields.Many2one('medical.consultation', string='Consultation')

    @api.depends('date')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = _('Evolution of %s') % rec.date

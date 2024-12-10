# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class MedicalConsultation(models.Model):
    _name = 'medical.consultation'
    _description = 'Medical Consultation'

    name = fields.Char(string='Name')
    date = fields.Date(string='Date')
    description = fields.Text(string='Description')
    medical_record_id = fields.Many2one('medical.record', string='Medical record')
    evolution_ids = fields.One2many('medical.evolution', 'consultation_id', string='Evolutions')

    @api.depends('date')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = _('Consultation of %s') % rec.date

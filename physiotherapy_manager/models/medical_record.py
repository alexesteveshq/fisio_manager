# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class MedicalRecord(models.Model):
    _name = 'medical.record'
    _description = 'Medical Record'
    _rec_name = 'patient_id'

    medic_id = fields.Many2one('res.partner', string='Medic')
    patient_id = fields.Many2one('res.partner', string='Patient')
    session_ids = fields.One2many('medical.record.session', 'medical_record_id', string='Sessions')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    age = fields.Integer(related='patient_id.age', store=True)
    vat = fields.Char(related='patient_id.vat', store=True, string='ID number')
    evaluation = fields.Text(string='Evaluation')
    diagnosis = fields.Text(string='Diagnosis')
    recipe = fields.Html(string='Recipe')
    consultation_ids = fields.One2many('medical.consultation', 'medical_record_id', string='Consultations')

    @api.depends('patient_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f'{rec.patient_id.name} record'

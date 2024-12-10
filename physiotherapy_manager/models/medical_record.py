# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class MedicalRecord(models.Model):
    _name = 'medical.record'
    _description = 'Medical Record'

    medic_id = fields.Many2one('res.partner', string='Medic')
    patient_id = fields.Many2one('res.partner', string='Patient')
    diagnosis = fields.Text(string='Diagnosis')
    evaluation = fields.Text(string='Evaluation')
    appointment_id = fields.Many2one('medical.appointment', string='Appointment')
    session_ids = fields.One2many('medical.record.session', 'medical_record_id', string='Sessions')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    age = fields.Integer(related='patient_id.age', store=True)
    vat = fields.Char(related='patient_id.vat', store=True, string='ID number')
    procedure_ids = fields.Many2many('medical.procedure', string='Procedures')
    recipe = fields.Html(string='Recipe')
    invoice_id = fields.Many2one('account.move', string='Invoices')
    consultation_ids = fields.One2many('medical.consultation', 'medical_record_id', string='Consultations')
    state = fields.Selection([('waiting', 'Waiting'), ('attended', 'Attended'),
                              ('not_attended', 'Not attended')], default='waiting')
    invoice_state = fields.Selection([('invoiced', 'Invoiced'),
                                      ('not_invoiced', 'Not invoiced')], default='not_invoiced')

    def open_consultation_invoice(self):
        self.ensure_one()
        return {
            'name': _('Invoice'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.invoice_id.id,
        }

    def invoice_generate(self):
        if not len(set(self.mapped('patient_id'))) <= 1:
            raise ValidationError(_("All consultations must belong to a same patient"))
        service = self.env['product.product'].search([('default_code', '=', 'consultation')])
        if not service:
            service = self.env['product.product'].create({'name': _('Consultation'),
                                                                  'default_code': 'consultation'})
        lines = []
        for consultation in self:
            lines.append((0, 0, {'product_id': service.id,
                                 'name': _('consultation'),
                                 'procedure_ids': consultation.procedure_ids.ids,
                                 'ensurance_id': consultation.patient_id.ensurance_id.id}))
        if lines:
            invoice = self.env['account.move'].create({'partner_id': self[0].patient_id.id,
                                                       'move_type': 'out_invoice',
                                                       'line_ids': lines})
            self.write({'invoice_id': invoice.id, 'invoice_state': 'invoiced'})

    @api.onchange('state')
    def onchange_state(self):
        self.appointment_id.state = self.state

    @api.depends('patient_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f'{rec.patient_id.name} record'

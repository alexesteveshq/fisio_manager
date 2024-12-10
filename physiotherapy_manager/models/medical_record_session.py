# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class MedicalRecord(models.Model):
    _name = 'medical.record.session'
    _description = 'Medical Record Session'

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    medical_record_id = fields.Many2one('medical.record', string='Medical record', ondelete='cascade')
    date = fields.Date(string='Date', default=fields.Date.today())
    appointment_id = fields.Many2one('medical.appointment', string='Appointment')
    therapist_id = fields.Many2one('res.partner', string='Therapist')
    pain_level = fields.Integer(string='Pain level')
    procedure_ids = fields.Many2many('medical.procedure', string='Procedures')
    patient_id = fields.Many2one(related='medical_record_id.patient_id', store=True)
    description = fields.Text(string='Description', index=True)
    observations = fields.Text(string='Observations')
    quantity = fields.Integer(string='Quantity', default=1)
    ensurance_id = fields.Many2one(related='patient_id.ensurance_id', store=True)
    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    state = fields.Selection([('waiting', 'Waiting'), ('attended', 'Attended'),
                              ('not_attended', 'Not attended')], default='waiting')
    invoice_state = fields.Selection([('invoiced', 'Invoiced'),
                                      ('not_invoiced', 'Not invoiced')], default='not_invoiced')
    invoice_id = fields.Many2one('account.move', string='Invoices')

    @api.onchange('state')
    def onchange_state(self):
        self.appointment_id.state = self.state

    def open_session_invoice(self):
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
            raise ValidationError(_("All sessions must belong to a same patient"))
        therapy_service = self.env['product.product'].search([('default_code', '=', 'therapy')])
        if not therapy_service:
            therapy_service = self.env['product.product'].create({'name': _('Physiotherapy'),
                                                                  'default_code': 'therapy'})
        lines = []
        for session in self:
            lines.append((0, 0, {'product_id': therapy_service.id,
                                 'name': session.description,
                                 'quantity': session.quantity,
                                 'procedure_ids': session.procedure_ids.ids,
                                 'ensurance_id': session.ensurance_id.id}))
        if lines:
            invoice = self.env['account.move'].create({'partner_id': self[0].patient_id.id,
                                                       'move_type': 'out_invoice',
                                                       'line_ids': lines})
            self.write({'invoice_id': invoice.id, 'invoice_state': 'invoiced'})

    @api.depends('patient_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f'{rec.patient_id.name} session'

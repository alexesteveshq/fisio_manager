# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class MedicalConsultation(models.Model):
    _name = 'medical.consultation'
    _description = 'Medical Consultation'

    name = fields.Char(string='Name')
    date = fields.Date(string='Date')
    medical_record_id = fields.Many2one('medical.record', string='Medical record')
    evolution_ids = fields.Many2many('medical.consultation', 'consultation_evolution_rel', 'consultation_id',
                                     'evolution_id',string='Evolutions')
    appointment_state = fields.Selection([('waiting', 'Waiting'), ('attended', 'Attended'),
                              ('not_attended', 'Not attended')], default='waiting')
    invoice_state = fields.Selection([('invoiced', 'Invoiced'),
                                      ('not_invoiced', 'Not invoiced')], default='not_invoiced')
    procedure_ids = fields.Many2many('medical.procedure', string='Procedures')
    invoice_id = fields.Many2one('account.move', string='Invoices')
    evaluation = fields.Text(string='Evaluation')
    diagnosis = fields.Text(string='Diagnosis')
    appointment_id = fields.Many2one('medical.appointment', string='Appointment')
    medic_id = fields.Many2one('res.partner', string='Medic')
    patient_id = fields.Many2one('res.partner', string='Patient')

    @api.depends('date')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = _('Consultation')
            if rec.date:
                rec.display_name = _('Consultation of %s' % rec.date)

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

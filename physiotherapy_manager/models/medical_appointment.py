# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime, timedelta


class MedicalAppointment(models.Model):
    _name = 'medical.appointment'
    _description = 'Medical Appointment'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    patient_id = fields.Many2one('res.partner', string='Patient')
    medic_id = fields.Many2one('res.partner', string='Medic')
    therapist_id = fields.Many2one('res.partner', string='Therapist')
    medical_record_id = fields.Many2one('medical.record', string='Medical record')
    consultation_id = fields.Many2one('medical.consultation', string='Consultation')
    session_id = fields.Many2one('medical.record.session', string='Session')
    type = fields.Selection([('consultation', 'Consultation'), ('therapy', 'Therapy')], string='Type')
    state = fields.Selection([('waiting', 'Waiting'), ('attended', 'Attended'),
                              ('not_attended', 'Not attended')], default='waiting')
    date_begin = fields.Datetime(string='Date begin')
    date_end = fields.Datetime(string='Date end')
    is_this_week = fields.Boolean(string="This Week", compute='_compute_is_this_week', store=True)
    day_name = fields.Char(string="Day Name", compute='_compute_day_name', store=True)

    @api.depends('date_begin')
    def _compute_day_name(self):
        day_map = {
            0: _('1. Monday'),
            1: _('2. Tuesday'),
            2: _('3. Wednesday'),
            3: _('4. Thursday'),
            4: _('5. Friday'),
            5: _('6. Saturday'),
            6: _('7. Sunday'),
        }
        for appointment in self:
            if appointment.date_begin:
                # Convert date to the day of the week and map to formatted string (e.g., '1. Monday')
                appointment_date = fields.Datetime.from_string(appointment.date_begin)
                day_number = appointment_date.weekday()  # Get day of the week (0=Monday, 6=Sunday)
                appointment.day_name = day_map[day_number]
            else:
                appointment.day_name = ''

    @api.depends('date_begin')
    def _compute_is_this_week(self):
        for appointment in self:
            if appointment.date_begin:
                today = datetime.today().date()  # Convert today's datetime to date
                start_of_week = today - timedelta(days=today.weekday())  # Monday of the current week as a date object
                end_of_week = start_of_week + timedelta(days=6)  # Sunday of the current week as a date object
                appointment_date = fields.Datetime.from_string(appointment.date_begin).date()
                appointment.is_this_week = start_of_week <= appointment_date <= end_of_week
            else:
                appointment.is_this_week = False

    @api.model_create_multi
    def create(self, vals):
        res = super(MedicalAppointment, self).create(vals)
        for appointment in res:
            if appointment.type == 'consultation':
                medical_record = self.env['medical.record'].search([('patient_id', '=', appointment.patient_id.id)])
                if not medical_record:
                    medical_record = self.env['medical.record'].create(
                        {'medic_id': appointment.medic_id.id,
                         'patient_id': appointment.patient_id.id})
                consultation = self.env['medical.consultation'].create(
                    {'medic_id': appointment.medic_id.id,
                     'date': appointment.date_begin,
                     'medical_record_id': medical_record.id,
                     'patient_id': appointment.patient_id.id,
                     'appointment_id': appointment.id})
                appointment.consultation_id = consultation.id
                appointment.medical_record_id = medical_record.id
            elif appointment.type == 'therapy':
                session = self.env['medical.record.session'].create(
                    {'therapist_id': appointment.therapist_id.id,
                     'medical_record_id': appointment.medical_record_id.id,
                     'appointment_id': appointment.id})
                appointment.session_id = session
                appointment.patient_id = appointment.consultation_id.patient_id
        return res

    @api.onchange('state')
    def onchange_state(self):
        if self.type == 'consultation':
            self.consultation_id.appointment_state = self.state
        elif self.type == 'therapy':
            self.session_id.state = self.state

    @api.depends('patient_id')
    def _compute_display_name(self):
        for rec in self:
            if rec.type == 'consultation':
                rec.display_name = f'{rec.patient_id.name} consultation'
            elif rec.type == 'therapy':
                rec.display_name = f'{rec.medical_record_id.patient_id.name} therapy'
            else:
                rec.display_name = f'Appointment'

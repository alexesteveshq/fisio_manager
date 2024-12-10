# -*- coding: utf-8 -*-
from odoo import fields, models


class MedicalEnsurance(models.Model):
    _name = 'medical.ensurance'
    _description = 'Medical Ensurance'

    name = fields.Char(string='name')

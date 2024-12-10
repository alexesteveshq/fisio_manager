# -*- coding: utf-8 -*-
from odoo import fields, models


class MedicalPathology(models.Model):
    _name = 'medical.pathology'
    _description = 'Medical Pathology'

    code = fields.Char(string='Code')
    name = fields.Char(string='Name')

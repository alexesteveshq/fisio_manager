# -*- coding: utf-8 -*-
from odoo import fields, models


class MedicalProcedure(models.Model):
    _name = 'medical.procedure'
    _description = 'Medical Procedure'

    name = fields.Char(string='name')

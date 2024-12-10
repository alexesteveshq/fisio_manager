# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Physiotherapy manager',
    'summary': 'Physiotherapy manager',
    'description': 'Physiotherapy manager',
    'category': 'Physiotherapy',
    'author': 'Alex Esteves',
    'depends': [
        'base', 'base_accounting_kit',
    ],
    'data': [
        'security/physiotherapy_manager.xml',
        'data/ir_action_data.xml',
        'security/ir.model.access.csv',
        'views/medical_record_view.xml',
        'views/medical_record_session_view.xml',
        'views/medical_appointment_view.xml',
        'views/medical_procedure_view.xml',
        'views/medical_ensurance_view.xml',
        'views/medical_pathology_view.xml',
        'views/medical_consultation_view.xml',
        'views/account_move_views.xml',
        'views/res_partner_views.xml',
        'views/menus.xml',
        'report/medical_record_report.xml',
        'report/medical_record_template.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
}

# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CompanyWorkplace(models.Model):
    _name = 'company.workplace'
    _description = 'Centro de Trabajo de Empresa'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    name = fields.Char(string='Nombre del Centro', required=True)
    sequence = fields.Integer(string='Secuencia', default=10)
    company_id = fields.Many2one('company.info', string='Empresa', required=True, ondelete='cascade')
    
    # Dirección
    street = fields.Char(string='Calle')
    city = fields.Char(string='Ciudad')
    state = fields.Char(string='Provincia')
    zip = fields.Char(string='Código Postal')
    country = fields.Char(string='País', default='España')
    
    # Contacto
    phone = fields.Char(string='Teléfono')
    email = fields.Char(string='Email')
    
    # Horarios
    company_schedule = fields.Char(string='Horario Empresa')
    student_schedule = fields.Char(string='Horario Alumnos')
    
    # Relación con tutores
    tutor_ids = fields.Many2many(
        'company.tutor',
        'workplace_tutor_rel',
        'workplace_id',
        'tutor_id',
        string='Tutores Asignados'
    )
    
    # Información adicional
    observations = fields.Text(string='Observaciones')
    active = fields.Boolean(string='Activo', default=True)
    
    @api.depends('name', 'city')
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.city:
                name = f"{name} ({record.city})"
            result.append((record.id, name))
        return result

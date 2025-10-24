# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CompanyTutor(models.Model):
    _name = 'company.tutor'
    _description = 'Tutor de Empresa'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Nombre Completo', required=True)
    dni = fields.Char(string='DNI/NIF')
    phone = fields.Char(string='Teléfono')
    email = fields.Char(string='Email')
    schedule = fields.Char(string='Horario')
    
    # Relación con empresa
    company_id = fields.Many2one('company.info', string='Empresa', required=True, ondelete='cascade')
    
    # Relación con centros de trabajo
    workplace_ids = fields.Many2many(
        'company.workplace',
        'workplace_tutor_rel',
        'tutor_id',
        'workplace_id',
        string='Centros de Trabajo Asignados'
    )
    
    # Información adicional
    position = fields.Char(string='Cargo/Puesto')
    observations = fields.Text(string='Observaciones')
    active = fields.Boolean(string='Activo', default=True)
    
    _sql_constraints = [
        ('dni_company_unique', 'unique(dni, company_id)', 'Ya existe un tutor con este DNI en la empresa.')
    ]

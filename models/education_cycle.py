# -*- coding: utf-8 -*-

from odoo import models, fields


class EducationCycle(models.Model):
    _name = 'education.cycle'
    _description = 'Ciclos Formativos'
    _order = 'sequence, name'

    name = fields.Char(string='Nombre del Ciclo', required=True)
    code = fields.Char(string='Código', required=True)
    level = fields.Selection([
        ('gm', 'Grado Medio'),
        ('gs', 'Grado Superior'),
    ], string='Nivel', required=True)
    sequence = fields.Integer(string='Secuencia', default=10)
    active = fields.Boolean(string='Activo', default=True)
    description = fields.Text(string='Descripción')
    
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'El código del ciclo ya existe.'),
    ]

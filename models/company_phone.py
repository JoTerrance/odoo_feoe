# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CompanyPhone(models.Model):
    _name = 'company.phone'
    _description = 'Teléfonos de Empresa'
    _order = 'sequence, phone_type, id'
    
    company_id = fields.Many2one(
        'company.info',
        string='Empresa',
        required=True,
        ondelete='cascade',
        help="Empresa a la que pertenece este teléfono"
    )
    
    phone = fields.Char(
        string='Teléfono',
        required=True,
        help="Número de teléfono"
    )
    
    phone_type = fields.Selection([
        ('principal', 'Principal'),
        ('alternative', 'Alternativo'),
        ('mobile', 'Móvil'),
        ('fax', 'Fax'),
        ('other', 'Otro')
    ], string='Tipo', default='principal', required=True,
       help="Tipo de teléfono")
    
    sequence = fields.Integer(
        string='Secuencia',
        default=10,
        help="Orden de visualización"
    )
    
    note = fields.Char(
        string='Nota',
        help="Información adicional sobre este teléfono"
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True,
        help="Si está desactivado, el teléfono no será visible"
    )
    
    _sql_constraints = [
        ('phone_company_unique', 'unique(phone, company_id)', 
         'Este teléfono ya está registrado para esta empresa!')
    ]
    
    def name_get(self):
        """Muestra el teléfono con su tipo"""
        result = []
        for record in self:
            type_label = dict(self._fields['phone_type'].selection).get(record.phone_type, '')
            name = f"{record.phone} ({type_label})"
            result.append((record.id, name))
        return result

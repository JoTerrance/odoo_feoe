# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CompanyFCTInterest(models.Model):
    _name = 'company.fct.interest'
    _description = 'Interés de Empresas en FCT/Prácticas'
    _order = 'company_id, cycle_id, course'

    # Relaciones
    company_id = fields.Many2one('company.info', string='Empresa', required=True, ondelete='cascade')
    cycle_id = fields.Many2one('education.cycle', string='Ciclo Formativo', required=True, ondelete='restrict')
    
    # Curso
    course = fields.Selection([
        ('1', '1º'),
        ('2', '2º'),
        ('dual', 'DUAL INTENSIVA'),
    ], string='Curso', required=True)
    
    # Convocatoria y año
    call = fields.Selection([
        ('first', 'Primera Convocatoria'),
        ('second', 'Segunda Convocatoria'),
    ], string='Convocatoria', required=True, default='first')
    
    year = fields.Integer(string='Año', required=True, default=lambda self: fields.Date.today().year,
                         help='Año en el que se mostró el interés')
    
    # Interés
    interested = fields.Boolean(string='Interesada en Acoger Alumnos', default=True)
    
    # Número de alumnos
    num_students = fields.Integer(string='Número de Alumnos')
    knows_number = fields.Boolean(string='Conoce el Número', default=False, 
                                   help='Marca si la empresa conoce el número exacto de alumnos que puede acoger')
    
    # Información adicional
    notes = fields.Text(string='Observaciones')
    
    # Campos relacionados para facilitar búsquedas
    company_name = fields.Char(related='company_id.name', string='Empresa', store=True, readonly=True)
    cycle_name = fields.Char(related='cycle_id.name', string='Ciclo', store=True, readonly=True)
    
    @api.constrains('num_students')
    def _check_num_students(self):
        for record in self:
            if record.num_students < 0:
                raise ValidationError('El número de alumnos no puede ser negativo.')
    
    @api.onchange('knows_number')
    def _onchange_knows_number(self):
        """Si no conoce el número, limpiar el campo"""
        if not self.knows_number:
            self.num_students = 0
    
    @api.onchange('interested')
    def _onchange_interested(self):
        """Si no está interesada, limpiar los campos relacionados"""
        if not self.interested:
            self.knows_number = False
            self.num_students = 0
    
    def name_get(self):
        """Personaliza el nombre mostrado del registro"""
        result = []
        for record in self:
            name = f"{record.cycle_id.code} - {record.course} - {record.year}"
            if record.call == 'second':
                name += " (2ª Conv)"
            if record.interested:
                if record.knows_number and record.num_students > 0:
                    name += f" ({record.num_students} alumnos)"
                else:
                    name += " (Interesada)"
            else:
                name += " (No interesada)"
            result.append((record.id, name))
        return result
    
    _sql_constraints = [
        ('company_cycle_course_call_year_unique', 
         'unique(company_id, cycle_id, course, call, year)', 
         'Ya existe un registro para esta empresa, ciclo, curso, convocatoria y año.'),
    ]

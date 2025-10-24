# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CompanyInfo(models.Model):
    _name = 'company.info'
    _description = 'Información de Empresas'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # Información básica
    name = fields.Char(string='Nombre de la Empresa', required=True, tracking=True)
    cif = fields.Char(string='CIF/NIF', tracking=True)
    
    # Contacto
    email = fields.Char(string='Email', tracking=True)
    phone = fields.Char(string='Teléfono Principal', tracking=True, help="Teléfono principal de contacto")
    phone_ids = fields.One2many(
        'company.phone',
        'company_id',
        string='Teléfonos',
        help="Lista de todos los teléfonos de contacto de la empresa"
    )
    mobile = fields.Char(string='Móvil', tracking=True)
    website = fields.Char(string='Sitio Web', tracking=True)
    
    # Dirección
    street = fields.Char(string='Calle', tracking=True)
    street2 = fields.Char(string='Calle 2', tracking=True)
    city = fields.Char(string='Ciudad', tracking=True)
    state_id = fields.Many2one('res.country.state', string='Provincia', tracking=True)
    zip = fields.Char(string='Código Postal', tracking=True)
    country_id = fields.Many2one('res.country', string='País', default=lambda self: self.env.ref('base.es').id, tracking=True)
    
    # Información empresarial
    sector = fields.Char(string='Sector/Actividad', tracking=True)
    num_employees = fields.Integer(string='Número de Empleados', tracking=True)
    annual_revenue = fields.Monetary(string='Facturación Anual', currency_field='currency_id', tracking=True)
    currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.company.currency_id)
    
    # Contacto principal en la empresa
    contact_person = fields.Char(string='Persona de Contacto', tracking=True)
    contact_position = fields.Char(string='Cargo', tracking=True)
    contact_email = fields.Char(string='Email de Contacto', tracking=True)
    contact_phone = fields.Char(string='Teléfono de Contacto', tracking=True)
    
    # Información específica de FCT (desde formulario)
    representative = fields.Char(string='Representante/Gerente', tracking=True, 
                                 help='Nombre completo del representante o gerente de la empresa')
    representative_nif = fields.Char(string='NIF Representante', tracking=True)
    tutor_fct = fields.Char(string='Tutor FCT', tracking=True,
                           help='Persona responsable de tutorizar las prácticas FCT')
    tutor_fct_nif = fields.Char(string='NIF Tutor FCT', tracking=True)
    rrhh_contact = fields.Char(string='Contacto RRHH', tracking=True,
                               help='Nombre del responsable de Recursos Humanos')
    rrhh_email = fields.Char(string='Email RRHH', tracking=True)
    rrhh_phone = fields.Char(string='Teléfono RRHH', tracking=True)
    activities = fields.Text(string='Actividades a Realizar',
                            help='Descripción de actividades que realizará el alumno en prácticas')
    schedule = fields.Char(string='Horario', tracking=True,
                          help='Horario de las prácticas FCT')
    company_schedule = fields.Char(string='Horario Empresa', tracking=True,
                                   help='Horario de trabajo de la empresa')
    student_schedule = fields.Char(string='Horario Alumnos', tracking=True,
                                   help='Horario para los alumnos en prácticas')
    observations = fields.Text(string='Observaciones',
                              help='Observaciones adicionales sobre las prácticas o la empresa')
    
    # Información adicional
    description = fields.Text(string='Descripción/Notas')
    active = fields.Boolean(string='Activo', default=True)
    
    # Estado de prospección
    stage = fields.Selection([
        ('new', 'Nueva'),
        ('contacted', 'Contactada'),
        ('qualified', 'Cualificada'),
        ('interested', 'Interesada'),
        ('negotiation', 'En Negociación'),
        ('won', 'Cliente'),
        ('lost', 'Perdida'),
    ], string='Estado', default='new', tracking=True)
    
    priority = fields.Selection([
        ('0', 'Baja'),
        ('1', 'Normal'),
        ('2', 'Alta'),
        ('3', 'Urgente'),
    ], string='Prioridad', default='1', tracking=True)
    
    # Responsable
    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user, tracking=True)
    
    # Relación con seguimientos
    tracking_ids = fields.One2many('company.tracking', 'company_id', string='Seguimientos')
    tracking_count = fields.Integer(string='Número de Seguimientos', compute='_compute_tracking_count')
    
    # Relación con interés en FCT/Prácticas
    fct_interest_ids = fields.One2many('company.fct.interest', 'company_id', string='Interés en FCT')
    fct_interest_count = fields.Integer(string='Ciclos con Interés', compute='_compute_fct_interest_count')
    
    # Relación con centros de trabajo y tutores
    workplace_ids = fields.One2many('company.workplace', 'company_id', string='Centros de Trabajo')
    workplace_count = fields.Integer(string='Número de Centros', compute='_compute_workplace_count')
    tutor_ids = fields.One2many('company.tutor', 'company_id', string='Tutores')
    tutor_count = fields.Integer(string='Número de Tutores', compute='_compute_tutor_count')
    
    # Fechas
    next_contact_date = fields.Date(string='Próximo Contacto', tracking=True)
    last_contact_date = fields.Date(string='Último Contacto', compute='_compute_last_contact_date', store=True)
    
    @api.depends('tracking_ids', 'tracking_ids.contact_date')
    def _compute_last_contact_date(self):
        for record in self:
            if record.tracking_ids:
                record.last_contact_date = max(record.tracking_ids.mapped('contact_date'))
            else:
                record.last_contact_date = False
    
    @api.depends('tracking_ids')
    def _compute_tracking_count(self):
        for record in self:
            record.tracking_count = len(record.tracking_ids)
    
    @api.depends('fct_interest_ids')
    def _compute_fct_interest_count(self):
        for record in self:
            record.fct_interest_count = len(record.fct_interest_ids.filtered('interested'))
    
    @api.depends('workplace_ids')
    def _compute_workplace_count(self):
        for record in self:
            record.workplace_count = len(record.workplace_ids)
    
    @api.depends('tutor_ids')
    def _compute_tutor_count(self):
        for record in self:
            record.tutor_count = len(record.tutor_ids)
    
    def action_view_trackings(self):
        """Acción para ver todos los seguimientos de esta empresa"""
        self.ensure_one()
        return {
            'name': 'Seguimientos',
            'type': 'ir.actions.act_window',
            'res_model': 'company.tracking',
            'view_mode': 'tree,form',
            'domain': [('company_id', '=', self.id)],
            'context': {'default_company_id': self.id},
        }
    
    def action_view_fct_interests(self):
        """Acción para ver todos los intereses en FCT de esta empresa"""
        self.ensure_one()
        return {
            'name': 'Interés en FCT/Prácticas',
            'type': 'ir.actions.act_window',
            'res_model': 'company.fct.interest',
            'view_mode': 'tree,form',
            'domain': [('company_id', '=', self.id)],
            'context': {'default_company_id': self.id},
        }
    
    def action_view_workplaces(self):
        """Acción para ver todos los centros de trabajo de esta empresa"""
        self.ensure_one()
        return {
            'name': 'Centros de Trabajo',
            'type': 'ir.actions.act_window',
            'res_model': 'company.workplace',
            'view_mode': 'tree,form',
            'domain': [('company_id', '=', self.id)],
            'context': {'default_company_id': self.id},
        }
    
    def action_view_tutors(self):
        """Acción para ver todos los tutores de esta empresa"""
        self.ensure_one()
        return {
            'name': 'Tutores',
            'type': 'ir.actions.act_window',
            'res_model': 'company.tutor',
            'view_mode': 'tree,form',
            'domain': [('company_id', '=', self.id)],
            'context': {'default_company_id': self.id},
        }
    
    _sql_constraints = [
        ('cif_unique', 'unique(cif)', 'El CIF ya existe en el sistema.'),
    ]

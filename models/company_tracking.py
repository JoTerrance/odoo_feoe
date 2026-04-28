# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CompanyTracking(models.Model):
    _name = 'company.tracking'
    _description = 'Seguimiento de Contactos con Empresas'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'contact_date desc, contact_time desc'

    # Relación con la empresa
    company_id = fields.Many2one('company.info', string='Empresa', required=True, ondelete='cascade', tracking=True)
    
    # Información del contacto
    contact_date = fields.Date(string='Fecha de Contacto', required=True, default=fields.Date.today, tracking=True)
    contact_time = fields.Float(string='Hora de Contacto', help='Hora en formato 24h (ej: 14.5 = 14:30)', tracking=True)
    
    # Responsable del contacto
    user_id = fields.Many2one('res.users', string='Contactado por', required=True, default=lambda self: self.env.user, tracking=True)
    
    # Tipo de contacto
    contact_type = fields.Selection([
        ('call', 'Llamada Telefónica'),
        ('email', 'Email'),
        ('meeting', 'Reunión Presencial'),
        ('video', 'Videollamada'),
        ('whatsapp', 'WhatsApp'),
        ('other', 'Otro'),
    ], string='Tipo de Contacto', required=True, default='call', tracking=True)
    
    # Temas tratados
    subject = fields.Char(string='Asunto', required=True, tracking=True)
    topics_discussed = fields.Text(string='Temas Tratados', required=True, tracking=True)
    
    # Resultado del contacto
    outcome = fields.Selection([
        ('positive', 'Positivo'),
        ('neutral', 'Neutral'),
        ('negative', 'Negativo'),
        ('pending', 'Pendiente de Respuesta'),
    ], string='Resultado', default='neutral', tracking=True)
    
    # Acciones a seguir
    next_action = fields.Text(string='Próximas Acciones')
    next_contact_date = fields.Date(string='Fecha Próximo Contacto')
    
    # Información adicional
    notes = fields.Text(string='Notas Adicionales')
    
    # Archivos adjuntos (ya incluido por defecto con mail.thread)
    attachment_ids = fields.Many2many('ir.attachment', string='Documentos Adjuntos')
    
    # Duración del contacto (en minutos)
    duration = fields.Integer(string='Duración (minutos)', help='Duración aproximada del contacto en minutos')
    
    # Campos relacionados para facilitar búsquedas
    company_name = fields.Char(related='company_id.name', string='Nombre Empresa', store=True, readonly=True)
    company_stage = fields.Selection(related='company_id.stage', string='Estado Empresa', readonly=True)
    
    @api.onchange('contact_date', 'contact_time')
    def _onchange_contact_datetime(self):
        """Actualiza la fecha del último contacto en la empresa"""
        if self.company_id and self.contact_date:
            # Esto se actualizará automáticamente mediante el compute en company.info
            pass
    
    @api.depends('company_id', 'company_id.name', 'contact_date', 'subject')
    def _compute_display_name(self):
        """Personaliza el nombre mostrado del registro"""
        for record in self:
            record.display_name = f"{record.company_id.name} - {record.contact_date} - {record.subject}"

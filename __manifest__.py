# -*- coding: utf-8 -*-
{
    'name': 'Gestión de Empresas FEOE',
    'version': '1.0',
    'category': 'CRM',
    'summary': 'Gestión y seguimiento de empresas para prospección',
    'description': """
        Módulo para gestionar información detallada de empresas y realizar
        seguimiento de contactos con las mismas.
        
        Características:
        - Registro completo de información empresarial
        - Seguimiento de contactos con fecha, hora y temas tratados
        - Historial de interacciones con cada empresa
        - Asignación de responsables para cada contacto
        - Gestión de interés en FCT/Prácticas por ciclos formativos
        - Control de número de alumnos que pueden acoger las empresas
    """,
    'author': 'FEOE',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/education_cycle_data.xml',
        'data/company_imported_data_combined.xml',
        'views/company_info_views.xml',
        'views/company_phone_views.xml',
        'security/company_phone_access.csv',
        'data/company_phones_data.xml',
        'data/fct_interest_imported_data.xml',
        'views/company_tracking_views.xml',
        'views/fct_views.xml',
        'views/company_fct_info_view.xml', 
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

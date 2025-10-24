# Gestión de Empresas FEOE

Módulo de Odoo para la gestión completa de empresas y seguimiento de contactos.

## Características

### 📋 Gestión de Empresas
- **Información completa**: Nombre, CIF, dirección, contacto, sector, número de empleados
- **Datos de contacto**: Teléfono, móvil, email, sitio web
- **Persona de contacto**: Datos del contacto principal en la empresa
- **Estados de prospección**: Nueva, Contactada, Interesada, En Negociación, Cliente, Perdida
- **Prioridades**: Baja, Normal, Alta, Urgente
- **Responsables**: Asignación de usuarios responsables de cada empresa

### 📞 Seguimiento de Contactos
- **Registro completo**: Fecha, hora y duración de cada contacto
- **Tipos de contacto**: Llamada, Email, Reunión Presencial, Videollamada, WhatsApp, Otro
- **Temas tratados**: Descripción detallada de lo que se habló
- **Resultados**: Positivo, Neutral, Negativo, Pendiente de Respuesta
- **Próximas acciones**: Planificación de acciones futuras
- **Responsables**: Registro de quién realizó el contacto
- **Adjuntos**: Posibilidad de adjuntar documentos

### 📊 Vistas y Reportes
- **Vista Lista**: Visualización rápida de todas las empresas
- **Vista Kanban**: Tarjetas visuales para gestión ágil
- **Vista Formulario**: Formulario completo con todos los detalles
- **Vista Calendario**: Calendario de seguimientos (solo para seguimientos)
- **Filtros avanzados**: Por estado, prioridad, responsable, fecha, etc.
- **Agrupaciones**: Por estado, ciudad, sector, responsable, etc.

## Instalación

1. Copia la carpeta `odoo_feoe` en el directorio `addons` de tu instalación de Odoo
2. Actualiza la lista de aplicaciones en Odoo
3. Busca "Gestión de Empresas FEOE" e instálalo

## Uso

### Crear una Empresa
1. Ve a **Gestión Empresas > Empresas**
2. Haz clic en **Crear**
3. Rellena la información de la empresa
4. Guarda

### Registrar un Seguimiento
1. Desde el formulario de una empresa, haz clic en el botón **Seguimientos**
2. Haz clic en **Crear**
3. Rellena los datos del contacto:
   - Fecha y hora
   - Tipo de contacto
   - Temas tratados
   - Resultado
4. Guarda

O bien:
1. Ve a **Gestión Empresas > Seguimientos**
2. Crea un nuevo seguimiento directamente

## Estructura del Módulo

```
odoo_feoe/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── company_info.py
│   └── company_tracking.py
├── views/
│   ├── company_info_views.xml
│   ├── company_tracking_views.xml
│   └── menus.xml
├── security/
│   └── ir.model.access.csv
└── README.md
```

## Modelos

### company.info
Modelo principal para almacenar información de empresas.

**Campos principales:**
- `name`: Nombre de la empresa
- `cif`: CIF/NIF
- `email`, `phone`, `mobile`, `website`: Datos de contacto
- `street`, `city`, `state_id`, `zip`, `country_id`: Dirección
- `sector`, `num_employees`, `annual_revenue`: Información empresarial
- `contact_person`, `contact_position`: Persona de contacto
- `stage`: Estado de prospección
- `priority`: Prioridad
- `user_id`: Responsable

### company.tracking
Modelo para registrar seguimientos de contactos.

**Campos principales:**
- `company_id`: Empresa relacionada
- `contact_date`: Fecha del contacto
- `contact_time`: Hora del contacto
- `user_id`: Quien realizó el contacto
- `contact_type`: Tipo de contacto
- `subject`: Asunto
- `topics_discussed`: Temas tratados
- `outcome`: Resultado
- `next_action`: Próximas acciones
- `duration`: Duración en minutos

## Dependencias

- `base`: Módulo base de Odoo
- `mail`: Para funcionalidades de chatter y seguimiento

## Versión

- **Versión**: 1.1
- **Compatible con**: Odoo 15.0+

## Licencia

LGPL-3

## Soporte

Para soporte y consultas, contacta con el equipo de desarrollo de FEOE.

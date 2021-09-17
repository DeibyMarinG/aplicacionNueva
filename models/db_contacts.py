# -*- coding: utf-8 -*-
db.define_table('Usuarios',
Field('nombre'),
Field('correo'),
Field('Numero_telefono'),
Field('Contraseña'),
Field('Fecha_nacimiento','date')
)
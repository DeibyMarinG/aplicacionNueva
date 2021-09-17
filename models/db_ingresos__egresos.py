# -*- coding: utf-8 -*-
db.define_table('ing_eg',
Field('tipo'),
Field('nombre'),
Field('monto','float'),
Field('recurrencia','integer'),
Field('empieza','date'),
Field('termina','date'),
Field('id_usuario','reference auth_user'),
Field('archivo','upload')
)
db.ing_eg.id_usuario.readable=db.ing_eg.id_usuario.writable=True



db.define_table('reporte',
Field('tipo'),
Field('nombre'),
Field('total','float'),
Field('recurrencia','integer'),
Field('empieza','date'),
Field('termina','date'),
Field('id_usuario','reference auth_user')
)

db.reporte.id_usuario.readable=db.reporte.id_usuario.writable=False
db.reporte.tipo.writable=False
db.reporte.total.writable=False


@auth.requires_login()
def reportes():
    db.ing_eg.id_usuario.default=auth.user.id
    db.ing_eg.id.readable=db.ing_eg.id.writable=False
    db.ing_eg.id_usuario.writable=False
    #db.ing_eg.empieza.readable=db.ing_eg.empieza.writable=False
    #db.ing_eg.termina.readable=db.ing_eg.termina.writable=False
    db.ing_eg.recurrencia.readable=db.ing_eg.recurrencia.writable=False
    db.ing_eg.tipo.requires = IS_IN_SET(['Activo', 'Pasivo'],
                     error_message='Error')
    db.ing_eg.monto.requires= IS_FLOAT_IN_RANGE(0.01, 10000000000.0,
                           error_message='negative or too large!')
    #db.ing_eg.id_usuario.widget= SQLFORM.widgets.autocomplete(request,auth.user.id)
    form = SQLFORM.grid(db.ing_eg, searchable=False,details=False,csv=False)
    
    return (dict(form=form))

def index():
    
    return(dict())
@auth.requires_login()
def graficos():
    from datetime import datetime
    form = SQLFORM.factory(
        Field('Fecha_inicio','date', requires=IS_NOT_EMPTY()),
        Field('Fecha_final','date', requires=IS_NOT_EMPTY()), Field('regla', requires=IS_IN_SET(['Solo en Rango', 'Atraviesen el rango'],
                     error_message='Error')))
    #if(contenedor_vars.grafico==None): 
    #    contenedor_vars.grafico='gantt'
    if form.process().accepted:
        fechainicio=datetime.strptime(str(form.vars.Fecha_inicio),'%d/%m/%Y')
        fechatermina=datetime.strptime(str(form.vars.Fecha_final),'%d/%m/%Y')
        if fechatermina>=fechainicio: 
            response.flash = 'form accepted'
            contenedor_vars.grafico='gantt'
            contenedor_vars.formulario=form
        else:
            response.flash = 'Fecha inicial debe ser menor que final'
    elif form.errors:
            response.flash = 'form has errors'
    return dict(form=form)

def gantt():
    formulario=contenedor_vars.formulario
    forma={'fecha_inicio':None,'fecha_final':None}
    if(formulario!=None):
        forma['fecha_inicio'] = formulario.Fecha_inicio
        forma['fecha_final'] = formulario.Fecha_final
        if(formulario.vars.regla=='Atraviesen el rango'):
            myquery=(db.ing_eg.id_usuario==auth.user.id) & ((formulario.Fecha_final>=db.ing_eg.empieza) & (formulario.Fecha_inicio <= db.ing_eg.termina))
        else:
            myquery=(db.ing_eg.id_usuario==auth.user.id) & ((formulario.Fecha_final>=db.ing_eg.termina) & (formulario.Fecha_inicio <=db.ing_eg.empieza ))

    else:
        myquery=(db.ing_eg.id_usuario==auth.user.id)
    forma['listado']= db(myquery).select()     
    return(dict(forma_grafico=forma))

def graficos_():
    if(contenedor_vars.grafico=='gantt'):
        gantt()
        return(dict())
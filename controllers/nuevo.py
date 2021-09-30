from datetime import datetime,timedelta

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
                     error_message='Error')),Field('grafico', requires=IS_IN_SET(['Gantt', 'Lineas'],
                     error_message='Error')))
    forma_grafico=None
    if(contenedor_vars.grafico==None): 
        contenedor_vars.grafico='gantt'
    if form.process().accepted:
        fechainicio=datetime.strptime(str(form.vars.Fecha_inicio),'%Y-%m-%d')
        fechatermina=datetime.strptime(str(form.vars.Fecha_final),'%Y-%m-%d')
        if fechatermina>=fechainicio: 
            response.flash = 'form accepted'  
            contenedor_vars.formulario=form
            forma_grafico=__escogergrafico(form.vars)
        else:
            response.flash = 'Fecha inicial debe ser menor que final'
    elif form.errors:
            response.flash = 'form has errors'
    return dict(form=form,forma_grafico=forma_grafico)

def __escogergrafico(formulario):
    if(formulario.grafico=='Gantt'):
        contenedor_vars.grafico='gantt'
        return(__gantt(formulario))
    elif(formulario.grafico=='Lineas'):
        contenedor_vars.grafico='lineas'
        return(__lineas(formulario))

def __gantt(formulario):
    #formulario=contenedor_vars.formulario
    forma={'fecha_inicio':None,'fecha_final':None}
    if(formulario!=None):
        forma['fecha_inicio'] = formulario.Fecha_inicio
        forma['fecha_final'] = formulario.Fecha_final
        if(formulario.regla=='Atraviesen el rango'):
            myquery=(db.ing_eg.id_usuario==auth.user.id) & ((formulario.Fecha_final>=db.ing_eg.empieza) & (formulario.Fecha_inicio <= db.ing_eg.termina))
        else:
            myquery=(db.ing_eg.id_usuario==auth.user.id) & ((formulario.Fecha_final>=db.ing_eg.termina) & (formulario.Fecha_inicio <=db.ing_eg.empieza ))
    else:
        myquery=(db.ing_eg.id_usuario==auth.user.id)
    forma['listado']= db(myquery).select()     
    return(forma)

def __lineas(formulario):

    diccionario_grafico={} 
    lista_activos_pasivos_usables={}
    if(formulario!=None):
        #response.flash = str(request.args(0)) 
        ########## aca se grafica ########
        visualizar=True
        empiezaR=formulario.Fecha_inicio
        terminaR=formulario.Fecha_final
        myquery=(db.ing_eg.id_usuario==auth.user.id)
        lista_activos_pasivos_usables= db(myquery).select()
        fechainicio=datetime.strptime(str(formulario.Fecha_inicio),'%Y-%m-%d')
        fechatermina=datetime.strptime(str(formulario.Fecha_final),'%Y-%m-%d')
        total=0
        dia_actual=fechainicio
        while (dia_actual<=fechatermina):
            for lista in lista_activos_pasivos_usables:
                i=datetime.strptime(str(lista.empieza),'%Y-%m-%d')
                while(i<=datetime.strptime(str(lista.termina),'%Y-%m-%d')):
                    if(dia_actual==i):
                        if(lista.tipo=='Activo'):
                            total=total+lista.monto
                        elif(lista.tipo=='Pasivo'):
                            total=total+lista.monto*-1
                        
                    i=i+timedelta(days=0)
            diccionario_grafico[dia_actual.strftime("new Date(%Y,%m,%d)")]=str(total)
            dia_actual=dia_actual+timedelta(days=1)
    return(diccionario_grafico)
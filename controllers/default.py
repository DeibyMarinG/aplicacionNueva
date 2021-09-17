# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
  
# ---- example index page ----

from datetime import timedelta


def index():
    #variable_123=234
    support_user= db(db.Usuarios.id==1).select()
    #users_name=all_users(0)['name']
    #response.flash = T("Hello World")
    redirect(URL('nuevo','index'))
    return locals() 
@auth.requires_login()
def reportes():
    from simple_examples import myplot4
    lista_activos_pasivos= db(db.ing_eg.id_usuario==auth.user.id).select()            
    lista_reportes= db(db.reporte.id_usuario==auth.user.id).select()
    #form1=SQLFORM(db.ing_eg)
    #myplot4()
    form1="Hola"
    if (request.vars.ok == '0' ):
        response.flash = "Error la fecha final es menor que la inicial"
    elif (request.vars.ok == '1'):
        response.flash = "Bien"
    if (request.vars.ok_del == '0' ):
        response.flash = "Eliminado registro de activos y pasivos"
    elif (request.vars.ok_del == '1' ):
        response.flash = "Eliminado registro de reportes"
    #else:
    #    response.flash = str(request.vars.ok_del) 

    return dict(lista_activos_pasivos=lista_activos_pasivos,lista_reportes=lista_reportes,form1=form1)
@auth.requires_login()
def ingreso_accion():
    from datetime import datetime
    fechainicio=datetime.strptime(str(request.vars.empieza),'%Y-%m-%d')
    fechatermina=datetime.strptime(str(request.vars.termina),'%Y-%m-%d')
    if(fechainicio>fechatermina):
        redirect(URL('reportes',vars=dict(ok=0)))
        #response.flash = T("Error la fecha final es menor que la inicial")
        return dict()
    if(request.vars.tipo=="on"):
        db.ing_eg.insert(nombre=request.vars.nombre,monto=request.vars.monto,recurrencia=request.vars.recurrencia,empieza=request.vars.empieza,termina=request.vars.termina,id_usuario=auth.user.id,tipo="Activo")
    else:
        db.ing_eg.insert(nombre=request.vars.nombre,monto=request.vars.monto,recurrencia=request.vars.recurrencia,empieza=request.vars.empieza,termina=request.vars.termina,id_usuario=auth.user.id,tipo="Pasivo")
    redirect(URL('reportes',vars=dict(ok=1)))
    return dict()
@auth.requires_login()
def ingreso_registro():
    from datetime import datetime, timedelta
    calculo=0
    myquery=(db.ing_eg.id_usuario==auth.user.id) & (db.ing_eg.termina >= request.vars.empieza_)
    lista_activos_pasivos_usables= db(myquery).select()    
    # for lista in lista_activos_pasivos_usables:
    #     if(lista.tipo=="Activo"):
    #         calculo=lista.monto+calculo
    #     elif(lista.tipo=="Pasivo"):
    #         calculo= lista.monto*-1 + calculo
    total=0
    dia_actual=datetime.strptime(str(request.vars.empieza_),'%Y-%m-%d')
    while (dia_actual<=datetime.strptime(str(request.vars.termina_),'%Y-%m-%d')):
        for lista in lista_activos_pasivos_usables:
            i=datetime.strptime(str(lista.empieza),'%Y-%m-%d')
            while(i<=datetime.strptime(str(lista.termina),'%Y-%m-%d')):
                if(dia_actual==i):
                    if(lista.tipo=='Activo'):
                        total=total+lista.monto
                    elif(lista.tipo=='Pasivo'):
                        total=total+lista.monto*-1
                    
                i=i+timedelta(days=lista.recurrencia)
        dia_actual=dia_actual+timedelta(days=1)
    if(request.vars.tipo_=="on"):
        db.reporte.insert(nombre=request.vars.nombre_,total=total,recurrencia=request.vars.recurrencia_,empieza=request.vars.empieza_,termina=request.vars.termina_,id_usuario=auth.user.id,tipo="Auto")
    else:
        db.reporte.insert(nombre=request.vars.nombre_,total=total,recurrencia=request.vars.recurrencia_,empieza=request.vars.empieza_,termina=request.vars.termina_,id_usuario=auth.user.id,tipo="Único")
    redirect(URL('reportes'))
    return dict()
@auth.requires_login()
def edit():
    if(request.vars.targetdb=='0'):
        ing_eg_e=db.ing_eg(request.args(0,cast=int))
        form=SQLFORM(db.ing_eg,ing_eg_e).process(next=URL('reportes'))
        texto="Activos y Pasivos"
    elif(request.vars.targetdb=='1'):
        reporte_e=db.reporte(request.args(0,cast=int))
        form=SQLFORM(db.reporte,reporte_e).process(next=URL('reportes'))
        texto="Reportes"
    return dict(form=form,texto=texto)
@auth.requires_login()
def recalcular_reporte():
    texto="error"
    if(request.vars.fuente=='0'):
        calculo=0
        reporte_sel=db(db.reporte.id == request.args(0)).select()
        empiezaR=reporte_sel[0].empieza
        terminaR=reporte_sel[0].termina
        myquery=(db.ing_eg.id_usuario==auth.user.id) & (db.ing_eg.empieza > empiezaR) & (db.ing_eg.termina <= terminaR)
        lista_activos_pasivos_usables= db(myquery).select()    
        for lista in lista_activos_pasivos_usables:
            if(lista.tipo=="Activo"):
                calculo=lista.monto+calculo
            elif(lista.tipo=="Pasivo"):
                calculo= lista.monto*-1 + calculo
        db(db.reporte.id == request.args(0)).update(total=calculo)
        redirect(URL('reportes',vars=dict(ok=1)))
        texto="Reportes"
    elif(request.vars.fuente=='1'):
        calculo=0
        reporte_sel=db(db.reporte.id == request.args(0)).select()
        empiezaR=reporte_sel[0].empieza
        terminaR=reporte_sel[0].termina
        myquery=(db.ing_eg.id_usuario==auth.user.id) & (db.ing_eg.empieza > empiezaR) & (db.ing_eg.termina <= terminaR)
        lista_activos_pasivos_usables= db(myquery).select()    
        for lista in lista_activos_pasivos_usables:
            if(lista.tipo=="Activo"):
                calculo=lista.monto+calculo
            elif(lista.tipo=="Pasivo"):
                calculo= lista.monto*-1 + calculo
        db(db.reporte.id == request.args(0)).update(total=calculo)
        redirect(URL('graficos',args=request.args(0)))
        texto="Reportes"
    return dict(texto=texto)
@auth.requires_login()   
def delete():
    if(request.vars.targetdb=='0'):
        db(db.ing_eg.id == request.args(0)).delete()
        redirect(URL('reportes',vars=dict(ok_del=0)))
        response.flash = "Eliminando en ing_eg"
    elif(request.vars.targetdb=='1'):
        db(db.reporte.id == request.args(0)).delete()
        response.flash = "eliminando en reportes"
        redirect(URL('reportes',vars=dict(ok_del=1)))
    return dict()
# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
@auth.requires_login()
def graficos():
    from datetime import datetime,timedelta
    from simple_examples import histogram
    lista_reportes= db(db.reporte.id_usuario==auth.user.id).select()
    #form1=SQLFORM(db.ing_eg)
  
    diccionario_grafico={} 
    lista_activos_pasivos_usables={}
    if(request.args(0)!=None):

        response.flash = str(request.args(0)) 
        ########## aca se grafica ########
        reporte=db(db.reporte.id==request.args(0)).select()
        visualizar=True
        empiezaR=reporte[0].empieza
        terminaR=reporte[0].termina
        myquery=(db.ing_eg.id_usuario==auth.user.id)
        lista_activos_pasivos_usables= db(myquery).select()
        fechainicio=datetime.strptime(str(reporte[0].empieza),'%Y-%m-%d')
        fechatermina=datetime.strptime(str(reporte[0].termina),'%Y-%m-%d')
        """  veces=fechatermina-fechainicio
            i=timedelta(days=0)
            form1=lista_activos_pasivos_usables
            while i<veces:
                dia=fechainicio+i
                i=i+timedelta(days=1)
                calculo=0      
                for lista in lista_activos_pasivos_usables:
                    dia_lista_e=datetime.strptime(str(lista.empieza),'%Y-%m-%d')
                    dia_lista_t=datetime.strptime(str(lista.termina),'%Y-%m-%d')
                    if((lista.tipo=="Activo")&(dia_lista_e<=dia)&(dia_lista_t>dia)):
                        calculo=calculo+lista.monto
                    elif((lista.tipo=="Pasivo")&(dia_lista_e<=dia)&(dia_lista_t>dia)):
                        calculo=calculo+lista.monto*-1
                diccionario_grafico[dia.strftime("new Date(%Y,%m,%d)")]=str(calculo)  """
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
                        
                    i=i+timedelta(days=lista.recurrencia)
            diccionario_grafico[dia_actual.strftime("new Date(%Y,%m,%d)")]=str(total)
            dia_actual=dia_actual+timedelta(days=1)




    else:
        #response.flash = str(request.vars.ok_del)
        visualizar=False 
        form1=1

    return dict(lista_reportes=lista_reportes,form1="Hola amigos",visualizar=visualizar,diccionario_grafico=diccionario_grafico,lista_activos_pasivos_usables=lista_activos_pasivos_usables)





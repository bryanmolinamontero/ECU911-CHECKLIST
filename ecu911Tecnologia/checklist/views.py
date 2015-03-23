# -*- coding: utf-8 -*-
# Create your views here.
from io import BytesIO
from django.core.mail import EmailMultiAlternatives

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4


from models import *

from reportlab.pdfgen import canvas

from reportlab.pdfgen import canvas
from django.http import HttpResponse

def reporte(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="reporte.pdf"'
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response,pagesize=A4)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    # pixeles de hoja A4 842x595
    p.drawString(10, 10, "Hello world.")

    #p.drawImage("http://mejoresimagenes.info/wp-content/uploads/2014/10/imagenes-con-frases-de-la-rana-rene.jpg",10,300)
    # Close the PDF object cleanly, and we're done.

    p.showPage()
    p.save()
    return response

def index(request):
    #registrosUsuarios = te_usuarios.objects.all().order_by("us_id")
    return render_to_response('index.html')


def tareas(request):
    registrosUsuarios = te_usuarios.objects.all().order_by("us_id")
    registrosLista = te_listas.objects.all().order_by("li_orden")
    return render_to_response('tareas.html',{"registrosUsuarios": registrosUsuarios, "registrosLista":registrosLista})


def tareaEspecifica(request):
    if request.POST:
        idUsuario = request.POST['usuario']
        nombreUsuario = te_usuarios.objects.get(us_id=idUsuario)
        fecha = request.POST['fecha']
        frecuencia = request.POST['frecuencia']
        idLista = request.POST['tarea']
        nombreLista = te_listas.objects.get(li_id=idLista)
        registosDeEsaTarea = te_tareas.objects.filter(ta_id_listas = idLista).order_by("ta_orden")

        verificadorDeInspeccionGuardada = te_inspeccion.objects.filter(in_id_contacto=idUsuario, in_nombre_usuario=nombreUsuario.us_usuario, in_fecha=fecha, in_id_lista = idLista)
        cont = 0
        for i in verificadorDeInspeccionGuardada:
            cont = cont + 1

        if cont==0:
            guardarInspeccion = te_inspeccion(in_id_contacto=idUsuario, in_nombre_usuario=nombreUsuario.us_usuario, in_fecha=fecha, in_frecuencia=frecuencia, in_id_lista = idLista)
            guardarInspeccion.save()  #SIRVE PARA VERIFICAR SI ES QUE EL USUARIO YA HA REALIZADO ESA INSPECCION
            obtenerInspeccionguardada = te_inspeccion.objects.get(in_id_contacto=idUsuario, in_nombre_usuario=nombreUsuario.us_usuario, in_fecha=fecha, in_frecuencia=frecuencia, in_id_lista = idLista)
            return render_to_response('tareaEspecifica.html',{ "nombreUsuario":nombreUsuario, "nombreLista":nombreLista, "fecha":fecha, "frecuencia":frecuencia,"idLista":idLista , "registrosDeEsaTarea":registosDeEsaTarea, "inspeccionGuardada":obtenerInspeccionguardada})

        else:
            obtenerInspeccionguardada = te_inspeccion.objects.get(in_id_contacto=idUsuario, in_nombre_usuario=nombreUsuario.us_usuario, in_fecha=fecha, in_frecuencia=frecuencia, in_id_lista = idLista)
            obtenerTodoslosDetallesDeLaInspeccion = te_detalle_inspeccion.objects.filter(de_id_inspeccion= obtenerInspeccionguardada.in_id)
            return render_to_response('tareaEspecifica.html',{ "nombreUsuario":nombreUsuario, "nombreLista":nombreLista, "fecha":fecha, "frecuencia":frecuencia,"idLista":idLista , "registrosDeEsaTarea":registosDeEsaTarea, "inspeccionGuardada":obtenerInspeccionguardada, "detallesDeEsaInspeccion":obtenerTodoslosDetallesDeLaInspeccion})



    else:
        return HttpResponseRedirect("/tareas/")



def guardarTareaEspecifica(request):
    if request.GET:
            try:
            #'idInspeccion': idInspeccion , 'idLista':idLista, 'idTarea':idTarea , 'tareaNombre':detalleTarea , 'descripcionTarea':descripcionTarea , 'resultado':resultado, 'observacion':observacion, 'fecha':fecha},
                idInspeccion =  request.GET['idInspeccion']
                idLista =  request.GET['idLista']
                idTarea =  request.GET['idTarea']
                tareaNombre =  request.GET['tareaNombre']
                descripcionTarea =  request.GET['descripcionTarea']
                resultado =  request.GET['resultado']
                observacion =  request.GET['observacion']
                fecha=  request.GET['fecha']

                print "***************"

                print idTarea
                print resultado
                print observacion

                print "***************"

                #SELECT ta_resultado_esperado FROM te_tareas WHERE ta_id = 105
                verificarResultadoEsperado = te_tareas.objects.get(ta_id = idTarea)
                if str(resultado) != str(verificarResultadoEsperado.ta_resultado_esperado) and observacion=="":
                    return HttpResponse("ResultadoNoEsperado")
                    print "ResultadoNoEsperado"
                else:
                    print "ResultadoEsperado"


                verificadorDeInspeccionGuardada = te_detalle_inspeccion.objects.filter(de_id_inspeccion = idInspeccion, de_id_listas = idLista, de_id_tareas = idTarea,  de_fecha= fecha)
                cont = 0
                for i in verificadorDeInspeccionGuardada:
                    cont = cont + 1

                if cont==0:
                    guardarDetalleInspeccion = te_detalle_inspeccion(de_id_inspeccion = idInspeccion, de_id_listas = idLista, de_id_tareas = idTarea, de_tarea_nombre = tareaNombre, de_tarea_descripcion = descripcionTarea, de_resultado = resultado, de_observacion = observacion, de_fecha= fecha)
                    guardarDetalleInspeccion.save()

                    #guardarAvance en la tabla turno
                    obtenerAvance = te_turno.objects.get(tu_fecha_turno=fecha)
                    print obtenerAvance.tu_avance
                    obtenerTareas = te_tareas.objects.count()
                    #regla de 3 para sacar el porcentaje de cada tarea para aumentar en avance
                    cadaTarea = 100/float(obtenerTareas)
                    avanceFinal = obtenerAvance.tu_avance + cadaTarea
                    avanceFinal = round(avanceFinal,2)
                    print "************"
                    print avanceFinal
                    print "************"
                    te_turno.objects.filter(tu_fecha_turno=fecha).update(tu_avance=avanceFinal)

                else:
                    te_detalle_inspeccion.objects.filter(de_id_inspeccion = idInspeccion, de_id_listas = idLista, de_id_tareas = idTarea,  de_fecha= fecha).update(de_resultado = resultado, de_observacion = observacion)

                return HttpResponse("True")
                '''de_id_inspeccion = models.IntegerField()
                    de_id_listas = models.IntegerField()
                    de_id_tareas = models.IntegerField()
                    de_tarea_nombre = models.CharField(max_length=250)
                    de_tarea_descripcion = models.CharField(max_length=250)
                    de_resultado = models.IntegerField()
                    de_observacion = models.CharField(max_length=500, blank=True)
                    de_fecha = models.DateField()
                   '''
            except:
                print "**** ERROR ****"
                return HttpResponse("False")
    else:
        return HttpResponseRedirect("/tareas/")


def validarDiaConUsuario(request):

    if request.GET:
        try:
            idUsuario =  request.GET['idUsuario']
            fecha =  request.GET['fecha']

            print idUsuario
            print fecha

            #verificamos si hay algun registro que en esa fecha tenga asociado ese id
            verificar = te_turno.objects.filter(tu_id_usuario=idUsuario, tu_fecha_turno=fecha)
            print verificar
            cont = 0
            for i in verificar:
                cont = cont + 1

            if cont > 0:
                return HttpResponse ("True")
            else:
                return HttpResponse ("False")

        except:
                print "**** ERROR ****"
                return HttpResponse("False")
    else:
        return HttpResponseRedirect("/tareas/")



import datetime
def calendario(request):
    registrosTurno = te_turno.objects.all()
    fechaActual = datetime.date.today()
    return render_to_response('calendario.html', {"registrosTurno":registrosTurno, "fechaActual": fechaActual})



def obtenerMalas(request):
    if request.GET:
        fecha = request.GET['fecha']
        from django.db import connection
        cursor = connection.cursor()
        sql = "SELECT SUM(ta_resultado_esperado <> de_resultado) FROM te_detalle_inspeccion JOIN te_inspeccion ON de_id_inspeccion=in_id JOIN te_tareas ON ta_id=de_id_tareas WHERE in_fecha='"+fecha+"' AND in_frecuencia='DIARIO' AND ta_resultado_esperado <> de_resultado"
        cursor.execute(sql)
        data = cursor.fetchall()
        return HttpResponse(data)
    else:
        return HttpResponseRedirect("/tareas/")


def obtenerBuenas(request):
    if request.GET:
        fecha = request.GET['fecha']
        from django.db import connection
        cursor = connection.cursor()
        sql = "SELECT SUM(ta_resultado_esperado = de_resultado) FROM te_detalle_inspeccion  JOIN te_inspeccion ON de_id_inspeccion=in_id JOIN te_tareas ON ta_id=de_id_tareas WHERE in_fecha='"+fecha+"' AND in_frecuencia='DIARIO' AND ta_resultado_esperado = de_resultado"
        cursor.execute(sql)
        data = cursor.fetchall()
        return HttpResponse(data)
    else:
        return HttpResponseRedirect("/tareas/")


def mostrarMalas(request):
    if request.GET:
        fecha = request.GET['fecha']

        usuario = te_turno.objects.get(tu_fecha_turno=fecha)
        from django.db import connection
        cursor = connection.cursor()
        sqlListas = "SELECT in_id, li_nombre  FROM te_inspeccion, te_listas WHERE in_fecha='"+fecha+"' AND te_inspeccion.in_id_lista=te_listas.li_id order by li_orden" #consulta que extrae todas las LISTAS DE ESE DIA
        cursor.execute(sqlListas)
        rowsListas = cursor.fetchall()
        import json
        rowarray_Listas = []
        for row in rowsListas:
            t = (row[0], row[1])
            rowarray_Listas.append(t)

        sqlTareas = "SELECT in_id, li_nombre, de_id, de_tarea_nombre, de_observacion FROM te_detalle_inspeccion JOIN te_listas ON li_id = de_id_listas  JOIN te_inspeccion ON de_id_inspeccion=in_id JOIN te_tareas ON ta_id=de_id_tareas WHERE in_fecha='"+fecha+"' AND in_frecuencia='DIARIO' AND ta_resultado_esperado <> de_resultado ORDER BY li_orden"
        cursor.execute(sqlTareas)
        rowsTareas = cursor.fetchall()
        import json
        rowarray_Tareas = []
        for row in rowsTareas:
            t = (row[0], row[1] , row[2] , row[3] , row[4])
            rowarray_Tareas.append(t)

        data = json.dumps({
        'listas': rowarray_Listas,
        'tareas': rowarray_Tareas,
        })

        return HttpResponse(data, mimetype='application/json')
    else:
        return HttpResponseRedirect("/tareas/")


def mostrarBuenas(request):
    if request.GET:
        fecha = request.GET['fecha']

        usuario = te_turno.objects.get(tu_fecha_turno=fecha)
        from django.db import connection
        cursor = connection.cursor()
        sqlListas = "SELECT in_id, li_nombre  FROM te_inspeccion, te_listas WHERE in_fecha='"+fecha+"' AND te_inspeccion.in_id_lista=te_listas.li_id order by li_orden" #consulta que extrae todas las LISTAS DE ESE DIA
        cursor.execute(sqlListas)
        rowsListas = cursor.fetchall()
        import json
        rowarray_Listas = []
        for row in rowsListas:
            t = (row[0], row[1])
            rowarray_Listas.append(t)

        sqlTareas = "SELECT in_id, li_nombre, de_id, de_tarea_nombre, de_observacion FROM te_detalle_inspeccion JOIN te_listas ON li_id = de_id_listas  JOIN te_inspeccion ON de_id_inspeccion=in_id JOIN te_tareas ON ta_id=de_id_tareas WHERE in_fecha='"+fecha+"' AND in_frecuencia='DIARIO' AND ta_resultado_esperado = de_resultado ORDER BY li_orden"
        cursor.execute(sqlTareas)
        rowsTareas = cursor.fetchall()
        import json
        rowarray_Tareas = []
        for row in rowsTareas:
            t = (row[0], row[1] , row[2] , row[3] , row[4])
            rowarray_Tareas.append(t)

        data = json.dumps({
        'listas': rowarray_Listas,
        'tareas': rowarray_Tareas,
        })

        return HttpResponse(data, mimetype='application/json')
    else:
        return HttpResponseRedirect("/tareas/")

def mostrarBuenas2(request):
    if request.GET:
        fecha = request.GET['fecha']
        from django.db import connection
        cursor = connection.cursor()
        sql = "SELECT  in_id, li_nombre, de_id, de_tarea_nombre, de_observacion FROM te_detalle_inspeccion JOIN te_listas ON li_id = de_id_listas  JOIN te_inspeccion ON de_id_inspeccion=in_id JOIN te_tareas ON ta_id=de_id_tareas WHERE in_fecha='"+fecha+"' AND in_frecuencia='DIARIO' AND ta_resultado_esperado = de_resultado order by li_orden"
        cursor.execute(sql)
        rows = cursor.fetchall()
        import json
        rowarray_list = []
        for row in rows:
            t = (row[0], row[1], row[2], row[3], row[4])
            rowarray_list.append(t)

        json_string = json.dumps(rowarray_list)
        return HttpResponse(json_string, mimetype='application/json')
    else:
        return HttpResponseRedirect("/tareas/")



def correo(request):
    registrosTurno = te_turno.objects.all()
    fechaActual = datetime.date.today()
    return render_to_response('correo.html', {"registrosTurno":registrosTurno, "fechaActual": fechaActual})

def enviarCorreo(request):
    if request.GET:
        try:
            fecha = request.GET['fecha']
            nombreUsuario = request.GET['nombreUsuario']
            registroCorreos = te_usuarios.objects.get(us_nombre=nombreUsuario)
            correo = registroCorreos.us_correo
            subject = 'Recordatorio CheckList'
            text_content = 'Sistema de CheckList'
            html_content = 'Estimado(a) ' + nombreUsuario + ' se le recuerda que el dia de hoy debe realizar el CheckList.<br> <a target="_blank" href="http://10.125.7.44:8000" > <br>Ir al Sistema</a> <hr> <h3>Att: Administrador de CheckList</h3>'
            from_email = '"origen" <dev.machala@ecu911.gob.ec>'
            #to = 'bryanux@hotmail.com'
            to = correo
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponse('True')
        except:
            return HttpResponse('False')
    else:
        return HttpResponseRedirect("/correo/")

def correoAutomatico(request):
        try:
            fecha = datetime.date.today()
            turnos = te_turno.objects.get(tu_fecha_turno=fecha)
            nombreUsuario = turnos.tu_nombre_usuario
            registroCorreos = te_usuarios.objects.get(us_nombre=nombreUsuario)
            correo = registroCorreos.us_correo
            subject = 'Recordatorio CheckList'
            text_content = 'Sistema de CheckList'
            html_content = 'Estimado(a) ' + nombreUsuario + ' se le recuerda que el dia de hoy debe realizar el CheckList.<br> <a target="_blank" href="http://10.125.7.44:8000" > <br>Ir al Sistema</a> <hr> <h3>Att: Administrador de CheckList</h3>'
            from_email = '"origen" <dev.machala@ecu911.gob.ec>'
            #to = 'bryanux@hotmail.com'
            to = correo
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponse('Correo Enviado')
        except:
            return HttpResponse('Correo No Enviado')

from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
Paragraph, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import os

def reportePorDia2(request, fecha):

        try:
            usuario = te_turno.objects.get(tu_fecha_turno=fecha)
            from django.db import connection
            cursor = connection.cursor()
            sqlListas = "SELECT in_id, li_nombre  FROM te_inspeccion, te_listas WHERE in_fecha='"+fecha+"' AND te_inspeccion.in_id_lista=te_listas.li_id order by li_orden" #consulta que extrae todas las LISTAS DE ESE DIA
            cursor.execute(sqlListas)
            rowsListas = cursor.fetchall()

            sqlTareasDeEsaLista = "SELECT de_tarea_nombre, de_tarea_descripcion, de_observacion, de_resultado, de_id_inspeccion FROM te_detalle_inspeccion WHERE de_fecha='"+fecha+"'"
            cursor.execute(sqlTareasDeEsaLista)
            rowsTareasDeEsaLista = cursor.fetchall()

            return render_to_response('reportePorDia.html',{"usuario":usuario, "registrosLista":rowsListas, "registrosTarea":rowsTareasDeEsaLista})
        except:
            return HttpResponseRedirect('/calendario/')



def reportePorDia(request, fecha):
        print "**********"
        print fecha
        print "**********"
        from django.db import connection
        cursor = connection.cursor()
        sqlListas = "SELECT in_id, li_nombre  FROM te_inspeccion, te_listas WHERE in_fecha='"+fecha+"' AND te_inspeccion.in_id_lista=te_listas.li_id order by li_nombre" #consulta que extrae todas las LISTAS DE ESE DIA
        cursor.execute(sqlListas)
        rowsListas = cursor.fetchall()

        #return render_to_response('reportePorDia.html',{"registros":rows})

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="reporte.pdf"'

        #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
        p = canvas.Canvas(response,pagesize=A4)

        # pixeles de hoja A4 595x842
        x = 30
        y = 750
        for i in rowsListas:
            p.drawString(x,y,i[1])
            y = y - 35

            sqlTareasDeEsaLista = "SELECT de_tarea_nombre, de_tarea_descripcion, de_observacion, de_resultado FROM te_detalle_inspeccion WHERE de_fecha='"+fecha+"' AND de_id_inspeccion = "+str(i[0]) + "order by de_tarea_nombre"
            cursor.execute(sqlTareasDeEsaLista)
            rowsTareasDeEsaLista = cursor.fetchall()

            for j in rowsTareasDeEsaLista:
                p.drawString(x,y,j[0])
                y = y - 35

                if y<=35:
                    y=750
                    p.showPage()


        #p.drawImage("http://mejoresimagenes.info/wp-content/uploads/2014/10/imagenes-con-frases-de-la-rana-rene.jpg",10,300)
        # Close the PDF object cleanly, and we're done.

        p.showPage()
        p.save()
        return response








def handler404(request):
    return render(request,'404.html')


# Create your views here.
from io import BytesIO


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

    drawing = Drawing(100, 200)
    data = [
    (13, 5, 20, 22, 37, 45, 19, 4),
    (14, 6, 21, 23, 38, 46, 20, 5)
    ]
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 300
    bc.data = data
    bc.strokeColor = colors.black
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 50
    bc.valueAxis.valueStep = 10
    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 8
    bc.categoryAxis.labels.dy = -2
    bc.categoryAxis.labels.angle = 30
    bc.categoryAxis.categoryNames = ['Jan-99','Feb-99','Mar-99',
    'Apr-99','May-99','Jun-99','Jul-99','Aug-99']
    drawing.add(bc)

    from reportlab.graphics import renderPDF
    renderPDF.drawToFile(drawing, 'reporte.pdf', 'My First Drawing')



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
                print idInspeccion
                print idLista
                print idTarea
                print tareaNombre
                print descripcionTarea
                print resultado
                print observacion
                print fecha
                print "***************"

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
    fecha = request.GET['fecha']
    from django.db import connection
    cursor = connection.cursor()
    sql = "SELECT SUM(ta_resultado_esperado <> de_resultado) FROM te_detalle_inspeccion JOIN te_inspeccion ON de_id_inspeccion=in_id JOIN te_tareas ON ta_id=de_id_tareas WHERE in_fecha='"+fecha+"' AND in_frecuencia='DIARIO' AND ta_resultado_esperado <> de_resultado"
    cursor.execute(sql)
    data = cursor.fetchall()
    return HttpResponse(data)


def obtenerBuenas(request):
    fecha = request.GET['fecha']
    from django.db import connection
    cursor = connection.cursor()
    sql = "SELECT SUM(ta_resultado_esperado = de_resultado) FROM te_detalle_inspeccion  JOIN te_inspeccion ON de_id_inspeccion=in_id JOIN te_tareas ON ta_id=de_id_tareas WHERE in_fecha='"+fecha+"' AND in_frecuencia='DIARIO' AND ta_resultado_esperado = de_resultado"
    cursor.execute(sql)
    data = cursor.fetchall()
    return HttpResponse(data)





def handler404(request):
    return render(request,'404.html')


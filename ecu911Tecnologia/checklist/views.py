# Create your views here.
from django.db.models.expressions import F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render

from models import *


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
    print "***********"
    print fechaActual
    print "***********"

    return render_to_response('calendario.html', {"registrosTurno":registrosTurno, "fechaActual": fechaActual})

def handler404(request):
    return render(request,'404.html')
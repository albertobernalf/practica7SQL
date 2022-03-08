from django.shortcuts import render
from django.shortcuts import render
import MySQLdb
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json
from django.views.generic import ListView, CreateView, TemplateView
from .forms import crearUsuariosForm
from datetime import datetime
from usuarios.models import Usuarios
from django.db.models import Max

from sitios.models import DependenciasActual, HistorialDependencias

# Create your views here.


class crearUsuarios(TemplateView):
    print("Entre a Crear el usuario")

    template_name = 'admisiones/crearUsuario.html'


    def post(self, request, *args, **kwargs):
        print("Entre POST de Crear Admisiones")
        data = {}
        context = {}
        #sedesClinica = request.POST['sedesClinica']
        sedesClinica = request.POST['Sede']
        Sede = request.POST['Sede']
        context['Sede'] = Sede
        Perfil = request.POST['Perfil']
        context['Perfil'] = Perfil


        print("Sedes Clinica = ", sedesClinica)
        print ("Sede = ",Sede)


        Username = request.POST["Username"]
        print(" = " , Username)
        context['Username'] = Username

        Username_id = request.POST["Username_id"]
        print("Username_id = ", Username_id)
        context['Username_id'] = Username_id



        tipoDoc = request.POST['tipoDoc']
        documento = request.POST['documento']
        print("tipoDoc = ", tipoDoc)
        print("documento = ", documento)




        usuarioRegistro = Username_id

        print("usuarioRegistro =", usuarioRegistro)
        now = datetime.now()
        dnow=now.strftime("%Y-%m-%d %H:%M:%S")
        print ("NOW  = ", dnow)

        fechaRegistro = dnow
        estadoReg = "A"
        print("estadoRegistro =", estadoReg)


        # VAmos a guardar el Usuarios

        grabo = Usuarios(
                         sedesClinica_id=Sede,
                         tipoDoc_id=tipoDoc,
                         documento_id=documento,
                         consec=consec,
                         fechaIngreso=fechaIngreso,
                         fechaSalida=fechaSalida,
                         factura=factura,
                         numcita=numcita,
                         dependenciasIngreso_id=dependenciasIngreso,
                         dxIngreso_id=dxIngreso,
                         medicoIngreso_id=medicoIngreso,
                         especialidadesMedicosIngreso_id=especialidadesMedicos,
                         dependenciasActual_id=dependenciasActual,
                         dxActual_id = dxActual,
                         medicoActual_id=medicoActual,
                         especialidadesMedicosActual_id=especialidadesMedicosActual,
                         dependenciasSalida_id = dependenciasSalida,
                         dxSalida_id = dxSalida,
                         medicoSalida_id=medicoSalida,
                         especialidadesMedicosSalida_id="",
                         estadoSalida_id = estadoSalida,

                         salidaClinica = salidaClinica,
                         salidaDefinitiva=salidaDefinitiva,
                         fechaRegistro=fechaRegistro,
                         usuarioRegistro_id=usuarioRegistro,
                         estadoReg=estadoReg

        )

        grabo.save()
        print("yA grabe 2", grabo.id)
        grabo.id

        # RUTINA ARMADO CONTEXT

        ingresos = []

        miConexionx = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable9')
        curx = miConexionx.cursor()


        detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag  , sitios_serviciosSedes sd WHERE  sd.sedesClinica_id = i.sedesClinica_id  and   sd.servicios_id  = ser.id and   i.sedesClinica_id = dep.sedesClinica_id AND i.dependenciasActual_id = dep.id AND i.sedesClinica_id= '" + str(
            Sede) + "'  AND  deptip.id = dep.dependenciasTipo_id and dep.servicios_id = ser.id AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and u.id = i.documento_id and diag.id = i.dxactual_id"
        print(detalle)

        curx.execute(detalle)

        for tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual in curx.fetchall():
            ingresos.append({'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,
                             'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida,
                             'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                             'DxActual': dxActual})

        miConexionx.close()
        print(ingresos)
        context['Ingresos'] = ingresos

        # Combo de Servicios
        miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable9')
        curt = miConexiont.cursor()
        comando = "SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed.sedesClinica_id ='" + str(Sede) + "' AND sed.servicios_id = ser.id"
        curt.execute(comando)
        print(comando)

        servicios = []
        servicios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            servicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(servicios)

        context['Servicios'] = servicios

        # Fin combo servicios

        # Combo de SubServicios
        miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable9')
        curt = miConexiont.cursor()
        comando = "SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed.sedesClinica_id ='" + str(
            Sede) + "' AND sed.servicios_id = ser.id and  sed.sedesClinica_id = sub.sedesClinica_id and sed.servicios_id =sub.servicios_id"
        curt.execute(comando)
        print(comando)

        subServicios = []
        subServicios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            subServicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(subServicios)

        context['SubServicios'] = subServicios

        # Fin combo SubServicios

        # Combo TiposDOc
        miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable9')
        curt = miConexiont.cursor()
        comando = "SELECT id ,nombre FROM usuarios_TiposDocumento "
        curt.execute(comando)
        print(comando)

        tiposDoc = []
        tiposDoc.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposDoc.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposDoc)

        context['TiposDoc'] = tiposDoc

        # Fin combo TiposDOc

        # Combo Habitaciones
        miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable9')
        curt = miConexiont.cursor()
        comando = "SELECT id ,nombre FROM sitios_dependencias where sedesClinica_id = '" + str(
            Sede) + "' AND dependenciasTipo_id = 2"
        curt.execute(comando)
        print(comando)

        habitaciones = []

        for id, nombre in curt.fetchall():
            habitaciones.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(habitaciones)

        context['Habitaciones'] = habitaciones

        # Fin combo Habitaciones

        # Combo Especialidades
        miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable9')
        curt = miConexiont.cursor()
        comando = "SELECT id ,nombre FROM clinico_Especialidades"
        curt.execute(comando)
        print(comando)

        especialidades = []
        especialidades.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            especialidades.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(especialidades)

        context['Especialidades'] = especialidades

        # Fin combo Especialidades

        # Combo Medicos
        miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable9')
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM planta_planta p ,  planta_perfilesplanta perf WHERE p.sedesClinica_id = perf.sedesClinica_id and  perf.sedesClinica_id = '" + str(
            Sede) + "' AND perf.tiposPlanta_id = 1   and p.id = perf.planta_id "

        curt.execute(comando)
        print(comando)

        medicos = []
        medicos.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            medicos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(medicos)

        context['Medicos'] = medicos

        # Fin combo Medicos

        # FIN RUTINA ARMADO CONTEXT


        return render(request, "admisiones/panelHospAdmisionesBravo.html", context)


    def get_context_data(self,  **kwargs):
        print("Entre a Contexto Usuarios")


        context = super().get_context_data(**kwargs)
        print(context['Sede'])
        Sede = context['Sede']
        Documento = context['Username']
        print ("Documento = ", Documento)

        context['Documento'] = Documento
        # Consigo la sede Nombre

        miConexion = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable9')
        cur = miConexion.cursor()
        comando = "SELECT id, nombre   FROM sitios_sedesClinica WHERE id ='" + Sede + "'"
        cur.execute(comando)
        print(comando)

        nombreSedes = []

        for id, nombre in cur.fetchall():
            nombreSedes.append({'id': id, 'nombre': nombre})

        miConexion.close()
        print(nombreSedes)

        context['NombreSede'] = nombreSedes

        print (context['NombreSede'])

        # Combo de Servicios
        miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable9')
        curt = miConexiont.cursor()
        comando = "SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed.sedesClinica_id ='" + str(Sede) + "' AND sed.servicios_id = ser.id"
        curt.execute(comando)
        print(comando)

        servicios = []
        servicios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            servicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(servicios)

        context['Servicios'] = servicios

        # Fin combo servicios

        # Combo Medicos
        miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable9')
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM planta_planta p ,  planta_perfilesplanta perf WHERE p.sedesClinica_id = perf.sedesClinica_id and  perf.sedesClinica_id = '" + str(
            Sede) + "' AND perf.tiposPlanta_id = 1   and p.id = perf.planta_id "

        curt.execute(comando)
        print(comando)

        medicos = []
        medicos.append({'id': '', 'nombre': ''})

        #for id, nombre in curt.fetchall():
        #    medicos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(medicos)

        context['Medicos'] = medicos

        # Fin combo Medicos

        # Combo Especialidades
        miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable9')
        curt = miConexiont.cursor()
        comando = "SELECT id ,nombre FROM clinico_Especialidades"
        curt.execute(comando)
        print(comando)

        especialidades = []
        especialidades.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            especialidades.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(especialidades)

        context['Especialidades'] = especialidades

        # Fin combo Especialidades

        context['title'] = 'Mi gran Template'
        context['form'] = crearUsuariosForm

        print("Se supone voya a cargar la forma de usuarios")
        print (context)
        return context

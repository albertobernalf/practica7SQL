from django.shortcuts import render
import MySQLdb
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json
from django.views.generic import ListView, CreateView, TemplateView
from .forms import crearAdmisionForm
from datetime import datetime
from admisiones.models import Ingresos
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.db.models.functions import Cast, Coalesce


from sitios.models import DependenciasActual, HistorialDependencias
from usuarios.models import Usuarios

# Create your views here.


def menuAcceso(request):
    print("Ingreso a acceso")


    miConexion = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM planta_tiposPlanta"
    cur.execute(comando)
    print(comando)

    perfiles = []
    context = {}

    for id, nombre in cur.fetchall():
        perfiles.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(perfiles)

    context['Perfiles'] = perfiles

    miConexion = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)

    sedes = []


    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes



    return render(request, "accesoPrincipal.html", context)




def validaAcceso(request):
    print("Hola Entre a validar el acceso Principal")

    username = request.POST["username"]
    print("username = ", username)
    contrasena = request.POST["password"]
    perfilConseguido = request.POST["seleccion1"]
    sede = request.POST["seleccion2"]
    Sede = sede
    print("Sede Mayuscula = ", Sede)
    print(contrasena)
    print("perfil= ", perfilConseguido)
    print("sede= ", sede)
    context = {}
    context['Documento'] = username
    context['Username'] = username
    context['Perfil'] = perfilConseguido
    context['Sede'] = sede

    # Variables que tengo en context : Documento, Perfil , Sede,   sedes ,NombreSede

    print (context['Documento'])

    # Consigo la sede Nombre

    miConexion = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    cur = miConexion.cursor()
    comando = "SELECT id, nombre   FROM sitios_sedesClinica WHERE id ='" + sede + "'"
    cur.execute(comando)
    print(comando)

    nombreSedes = []


    for id, nombre  in cur.fetchall():
        nombreSedes.append({'id':id , 'nombre' : nombre})

    miConexion.close()
    print(nombreSedes)

    context['NombreSede'] =  nombreSedes




    # esta consulta por que se pierde de otras pantallas

    miConexion = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)

    sedes = []

    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes


    miConexion = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM planta_tiposPlanta"
    cur.execute(comando)
    print(comando)

    perfiles = []


    for id, nombre in cur.fetchall():
        perfiles.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(perfiles)

    context['Perfiles'] = perfiles

    miConexion0 = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    cur0 = miConexion0.cursor()
    comando = "select p.id  Username_id , p.nombre profesional from planta_planta p where p.documento ='" + username + "'"
    cur0.execute(comando)
    print(comando)
    planta = []

    for Username_id, profesional in cur0.fetchall():
        planta.append({'Username_id': Username_id, 'profesional': profesional})
        context['Username_id'] = Username_id
        context['Profesional'] = profesional

    print ("Profesional = ", profesional )

    if planta == []:


        context['Error'] = "Personal invalido ! "
        print("Entre por personal No encontrado")

        miConexion0.close()

        return render(request, "accesoPrincipal.html", context)

    else:

        print("Username_id", Username_id)

        miConexion1 = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
        cur1 = miConexion1.cursor()
        comando = "select p.contrasena contrasena from planta_planta p where p.documento ='" + username + "'" + " AND contrasena = '" + contrasena +"'"
        cur1.execute(comando)

        plantaContrasena = []

        for nombre in cur1.fetchall():
            plantaContrasena.append({'contrasena': contrasena})

        if plantaContrasena == []:
            miConexion1.close()
            context['Error'] = "Contraseña invalida ! "
            return render(request, "accesoPrincipal.html", context)
        else:


            miConexion2 = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
            cur2 = miConexion1.cursor()
            comando = "select perf.tiposPlanta_id  perfil from planta_planta p , planta_perfilesplanta perf , planta_tiposPlanta tp where  p.sedesClinica_id = perf.sedesClinica_id and  p.sedesClinica_id ='" + str(sede) + "' AND p.documento =  '" + str(username) + "' AND perf.planta_id = p.id AND  perf.tiposPlanta_id = " + str(perfilConseguido)
            print(comando)
            cur2.execute(comando)

            perfil = []

            for perfil in cur2.fetchall():
                plantaContrasena.append({'perfil': perfil})


            if perfil == []:
                miConexion0.close()
                miConexion1.close()
                miConexion2.close()
                context['Error'] = "Perfil No autorizado ! "
                return render(request, "accesoPrincipal.html", context)


            else:

                ingresos = []

                miConexionx = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
                curx = miConexionx.cursor()

              #  detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , dxIngreso_id FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp  WHERE i.sedesClinica_id = dep.sedesClinica_id AND i.serviciosActual_id = dep.servicios_id AND i.serviciosActual_id = ser.id  AND i.dependenciasActual_id = dep.id AND i.sedesClinica_id= '" +  str(Sede) + "' AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id"

                #detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag  WHERE i.sedesClinica_id = dep.sedesClinica_id AND i.serviciosActual_id = dep.servicios_id AND i.serviciosActual_id = ser.id  AND i.dependenciasActual_id = dep.id AND  i.dependenciasIngreso_id = dep.id AND i.sedesClinica_id= '" + str( Sede) + "' AND dep.sedesClinica_id = i.sedesClinica_id AND i.sedesClinica_id = ser.sedesClinica_id AND deptip.id = dep.dependenciasTipo_id  AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and diag.id = i.dxactual_id"
                detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd.sedesClinica_id = i.sedesClinica_id  and   sd.servicios_id  = ser.id and  i.sedesClinica_id = dep.sedesClinica_id AND i.dependenciasActual_id = dep.id AND i.sedesClinica_id= '" + str(Sede) + "'  AND  deptip.id = dep.dependenciasTipo_id and dep.servicios_id = ser.id AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and u.id = i.documento_id and diag.id = i.dxactual_id"
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
                miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
                curt = miConexiont.cursor()
                comando = "SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed.sedesClinica_id ='" + str(sede) + "' AND sed.servicios_id = ser.id"
                curt.execute(comando)
                print(comando)

                servicios = []
                servicios.append({'id':'' , 'nombre': ''})

                for id, nombre in curt.fetchall():
                    servicios.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(servicios)

                context['Servicios'] = servicios

                # Fin combo servicios

                # Combo de SubServicios
                miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
                curt = miConexiont.cursor()
                comando = "SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed.sedesClinica_id ='" + str(
                    sede) + "' AND sed.servicios_id = ser.id and  sed.sedesClinica_id = sub.sedesClinica_id and sed.servicios_id =sub.servicios_id"
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
                miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
                curt = miConexiont.cursor()
                comando = "SELECT id ,nombre FROM usuarios_TiposDocumento "
                curt.execute(comando)
                print(comando)

                tiposDoc = []
                #tiposDoc.append({'id': '', 'nombre': ''})



                for id, nombre in curt.fetchall():
                    tiposDoc.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(tiposDoc)

                context['TiposDoc'] = tiposDoc

                # Fin combo TiposDOc

                # Combo Habitaciones
                miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
                curt = miConexiont.cursor()
                comando = "SELECT id ,nombre FROM sitios_dependencias where sedesClinica_id = '" + str(Sede) +"' AND dependenciasTipo_id = 2"
                curt.execute(comando)
                print(comando)

                habitaciones = []
                habitaciones.append({'id': '', 'nombre': ''})

                for id, nombre in curt.fetchall():
                    habitaciones.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(habitaciones)

                context['Habitaciones'] = habitaciones


                # Fin combo Habitaciones

                # Combo Especialidades
                miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
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



                # Combo EspecialidadesMedicos

                miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
                curt = miConexiont.cursor()
                comando = "SELECT em.id ,e.nombre FROM clinico_Especialidades e, clinico_EspecialidadesMedicos em,planta_planta pl  where em.especialidades_id = e.id and em.planta_id = pl.id AND pl.documento = '" + str(username) + "'"
                curt.execute(comando)
                print(comando)

                especialidadesMedicos = []
                especialidadesMedicos.append({'id': '', 'nombre': ''})

                for id, nombre in curt.fetchall():
                    especialidadesMedicos.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(especialidadesMedicos)

                context['EspecialidadesMedicos'] = especialidadesMedicos

                # Fin combo EspecialidadesMedicos


                # Combo Medicos
                miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
                curt = miConexiont.cursor()
                comando = "SELECT p.id id, p.nombre  nombre FROM planta_planta p ,  planta_perfilesplanta perf WHERE p.sedesClinica_id = perf.sedesClinica_id and  perf.sedesClinica_id = '" + str(Sede) + "' AND perf.tiposPlanta_id = 1 and p.id = perf.planta_id"

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

                # Combo TiposFolio

                miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
                curt = miConexiont.cursor()

                comando = "SELECT e.id id, e.nombre nombre FROM clinico_tiposFolio e"

                curt.execute(comando)
                print(comando)

                tiposFolio = []
                tiposFolio.append({'id': '', 'nombre': ''})

                for id, nombre in curt.fetchall():
                    tiposFolio.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(tiposFolio)

                context['TiposFolio'] = tiposFolio

                # Fin combo TiposFolio

                # Combo TiposUsuario

                miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
                curt = miConexiont.cursor()

                comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposusuario p"

                curt.execute(comando)
                print(comando)

                tiposUsuario = []
                # tiposUsuario.append({'id': '', 'nombre': ''})

                for id, nombre in curt.fetchall():
                    tiposUsuario.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(tiposUsuario)

                context['TiposUsuario'] = tiposUsuario

                # Fin combo Tipos Usuario

                # Combo TiposDocumento

                miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
                curt = miConexiont.cursor()

                comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposDocumento p"

                curt.execute(comando)
                print(comando)

                tiposDocumento = []
                #tiposDocumento.append({'id': '', 'nombre': ''})

                for id, nombre in curt.fetchall():
                    tiposDocumento.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(tiposDocumento)

                context['TiposDocumento'] = tiposDocumento

                # Fin combo TiposDocumento

                # Combo Centros

                miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
                curt = miConexiont.cursor()

                comando = "SELECT p.id id, p.nombre  nombre FROM sitios_centros p"

                curt.execute(comando)
                print(comando)

                centros = []

                for id, nombre in curt.fetchall():
                    centros.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(tiposDocumento)

                context['Centros'] = centros

                # Fin combo Centros

                # Combo Diagnosticos

                miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
                curt = miConexiont.cursor()

                comando = "SELECT p.id id, p.nombre  nombre FROM clinico_diagnosticos p"

                curt.execute(comando)
                print(comando)

                diagnosticos = []
                diagnosticos.append({'id': '', 'nombre': ''})

                for id, nombre in curt.fetchall():
                    diagnosticos.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(diagnosticos)

                context['Diagnosticos'] = diagnosticos

                # Fin combo Diagnosticos

                # Combo Departamentos

                miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
                curt = miConexiont.cursor()

                comando = "SELECT d.id id, d.nombre  nombre FROM sitios_departamentos d"

                curt.execute(comando)
                print(comando)

                departamentos = []
                # tiposDocumento.append({'id': '', 'nombre': ''})

                for id, nombre in curt.fetchall():
                    departamentos.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(departamentos)

                context['Departamentos'] = departamentos

                # Fin combo Departamentos

                # Combo Ciudades

                miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
                curt = miConexiont.cursor()

                comando = "SELECT c.id id, c.nombre  nombre FROM sitios_ciudades c"

                curt.execute(comando)
                print(comando)

                ciudades = []


                for id, nombre in curt.fetchall():
                    ciudades.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(ciudades)

                context['Ciudades'] = ciudades

                # Fin combo Ciudades

                print (perfil[0])

                if (perfil[0] == 1):
                    miConexion0.close()
                    miConexion1.close()
                    miConexion2.close()
                    print("voy para ")
                    return render(request, "clinico/panelClinico.html", context)
                if (perfil[0] == 2):
                    miConexion0.close()
                    miConexion1.close()
                    miConexion2.close()
                    return render(request, "clinico/menuEnfermero.html", context)
                if (perfil[0] == 3):
                    miConexion0.close()
                    miConexion1.close()
                    miConexion2.close()
                    return render(request, "clinico/menuAuxiliar.html", context)
                if (perfil[0] == 4):
                    miConexion0.close()
                    miConexion1.close()
                    miConexion2.close()
                    return render(request, "citasMedicas/menuCitasMedicas.html")
                if (perfil[0] == 5):
                    miConexion0.close()
                    miConexion1.close()
                    miConexion2.close()
                    return render(request, "facturacion/menuFacturacion.html", context)

                if (perfil[0] == 6):
                    miConexion0.close()
                    miConexion1.close()
                    miConexion2.close()
                    return render(request, "admisiones/panelAdmisiones.html", context)

    return render(request, "admisiones/panelAdmisiones.html",context)


def retornarAdmision(request, Sede, Perfil, Username, Username_id, NombreSede):


    print ("Entre Retornar Admision")
    #Sede = request.POST["Sede"]
    print ("Sede = ", Sede)
    Sede = Sede.lstrip()
    sede = Sede
    #Perfil = request.POST["Perfil"]
    print ("Perfil = ",Perfil)
    Perfil = Perfil.lstrip()
    print("Perfil = ", Perfil)

    print ("Nombre dede = ", NombreSede)

    context = {}

    context['Sede'] = Sede
    context['Username'] = Username
    context['Username_id'] = Username_id
    context['NombreSede'] = NombreSede


    # Consigo la sede Nombre

    miConexion = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    cur = miConexion.cursor()
    comando = "SELECT nombre   FROM sitios_sedesClinica WHERE id ='" + sede + "'"
    cur.execute(comando)
    print(comando)

    nombreSedes = []

    for nombre in cur.fetchall():
        nombreSedes.append({'nombre': nombre})

    miConexion.close()
    print(nombreSedes)
    nombresede1 = nombreSedes[0]

    context['NombreSede'] = nombresede1

    # esta consulta por que se pierde de otras pantallas

    miConexion = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)

    sedes = []

    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes

    ingresos = []

    miConexionx = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    curx = miConexionx.cursor()

    #  detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , dxIngreso_id FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp  WHERE i.sedesClinica_id = dep.sedesClinica_id AND i.serviciosActual_id = dep.servicios_id AND i.serviciosActual_id = ser.id  AND i.dependenciasActual_id = dep.id AND i.sedesClinica_id= '" +  str(Sede) + "' AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id"

    # detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag  WHERE i.sedesClinica_id = dep.sedesClinica_id AND i.serviciosActual_id = dep.servicios_id AND i.serviciosActual_id = ser.id  AND i.dependenciasActual_id = dep.id AND  i.dependenciasIngreso_id = dep.id AND i.sedesClinica_id= '" + str( Sede) + "' AND dep.sedesClinica_id = i.sedesClinica_id AND i.sedesClinica_id = ser.sedesClinica_id AND deptip.id = dep.dependenciasTipo_id  AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and diag.id = i.dxactual_id"
    detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag  WHERE i.sedesClinica_id = dep.sedesClinica_id AND i.dependenciasActual_id = dep.id AND i.sedesClinica_id= '" + str(
        Sede) + "'   AND deptip.id = dep.dependenciasTipo_id and dep.servicios_id = ser.id AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and u.id = i.documento_id and diag.id = i.dxactual_id"
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
    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    curt = miConexiont.cursor()
    comando = "SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed.sedesClinica_id ='" + str(
        sede) + "' AND sed.servicios_id = ser.id"
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
    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
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
    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
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
    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
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
    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
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
    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    curt = miConexiont.cursor()
    comando = "SELECT p.id id, p.nombre  nombre FROM planta_planta p ,  planta_perfilesplanta perf WHERE perf.sedesClinica_id = '" + str(
        Sede) + "' AND perf.tiposPlanta_id = 1 and p.id = perf.planta_id"

    curt.execute(comando)
    print(comando)

    medicos = []
    medicos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        medicos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(medicos)

    context['Medicos'] = medicos
    context['Perfil'] = Perfil

    # Fin combo Medicos

    if (Perfil == 1):
        return render(request, "menuMedico.html", context)
    if (Perfil == 2):
        return render(request, "menuEnfermero.html", context)
    if (Perfil == 3):
        return render(request, "menuAuxiliar.html", context)
    if (Perfil == 4):
        return render(request, "citasMedicas/menuCitasMedicas.html", context)
    if (Perfil == 5):
        return render(request, "facturacion/menuFacturacion.html", context)
    if (Perfil == 6):
        print ("Entre por dende ERA")
        return render(request, "admisiones/panelAdmisiones.html", context)

    return render(request, "admisiones/panelAdmisiones.html", context)


def salir(request):
    print("Voy a Salir")

    miConexion = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM planta_tiposPlanta"
    cur.execute(comando)
    print(comando)

    perfiles = []
    context = {}

    for id, nombre in cur.fetchall():
        perfiles.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(perfiles)

    context['Perfiles'] = perfiles

    miConexion = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)

    sedes = []

    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes





    return render(request, "accesoPrincipal.html", context)



def validaPassword(request, username, contrasenaAnt,contrasenaNueva,contrasenaNueva2):
    print("Entre ValidaPassword" )
    username = request.POST["username"]
    contrasenaAnt = request.POST["contrasenaAnt"]
    contrasenaNueva = request.POST["contrasenaNueva"]
    contrasenaNueva2 = request.POST["contrasenaNueva2"]

    print(username)
    print(contrasenaAnt)
    print(contrasenaNueva)
    print(contrasenaNueva2)
    context = {}

    if (contrasenaNueva2 != contrasenaNueva):
        dato = "No coinciden las contraseñas ! "
        context['Error'] = "No coincideln las contraseñas ! "
        print(context)

        return HttpResponse(dato)


    miConexion1 = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    cur1 = miConexion1.cursor()
    comando = "SELECT documento,contrasena FROM planta_planta WHERE documento = '" + str(username) + "'"
    print(comando)
    cur1.execute(comando)

    UsuariosHc = []

    for documento, contrasena in cur1.fetchall():
        UsuariosHc = {'username': documento, 'contrasena': contrasena}

    miConexion1.close()
    print(UsuariosHc)

    if UsuariosHc == []:

        dato = "Personal invalido ! "
        context['Error'] = "Personal invalido ! "
        print(context)

        return HttpResponse(dato)
        #return render(request, "accesoPrincipal.html", context)

    else:
        miConexion1 = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
        cur1 = miConexion1.cursor()
        comando = "SELECT documento,contrasena FROM planta_planta WHERE documento = '" + str(username) + "' AND contrasena = '" + str(contrasenaAnt) + "'"
        print(comando)
        cur1.execute(comando)

        ContrasenaHc = []
        for documento, contrasena in cur1.fetchall():
            ContrasenaHc = {'username': documento, 'contrasena': contrasena}
        miConexion1.close()

        if ContrasenaHc == []:
            dato = "Contraseña Invalida ! "
            context['Error'] = "Contraseña Invalida ! "
            print(context)

            return HttpResponse(dato)

        else:

            miConexion1 = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
            cur1 = miConexion1.cursor()
            comando = "UPDATE planta_planta SET contrasena = '" +  str(contrasenaNueva) + "' WHERE documento = '" + str(username) + "'"
            print(comando)
            cur1.execute(comando)
            miConexion1.commit()
            miConexion1.close()
            context['Error'] = "Contraseña Actualizada ! "
            dato = "Contraseña Actualizada !"
            print(context)
            #return HttpResponse(context, safe=False)
            return HttpResponse(dato)
            #return render(request, "accesoPrincipal.html", context)


    #return JsonResponse(UsuariosHc, safe=False)

def Modal(request, username, password):

        print("Entre a Modal")
        print(username)
        print(password)

        miConexion1 = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
        cur1 = miConexion1.cursor()
        comando = "SELECT documento,contrasena FROM planta_planta WHERE documento = '" + str(username) + "'"
        print(comando)
        cur1.execute(comando)

        UsuariosHc = {}

        for documento, contrasena in cur1.fetchall():
            UsuariosHc = {'username': documento, 'contrasena': contrasena}

        miConexion1.close()
        print(UsuariosHc)
        return JsonResponse(UsuariosHc, safe=False)
        # return HttpResponse(UsuariosHc)



def buscarAdmision(request):
    context = {}


    print("Entre Buscar Admision" )
    BusTipoDoc = request.POST["busTipoDoc"]
    BusDocumento = request.POST["busDocumento"]
    BusHabitacion = request.POST["busHabitacion"]



    BusDesde = request.POST["busDesde"]
    BusHasta = request.POST["busHasta"]
    BusEspecialidad = request.POST["busEspecialidad"]
    print ("Especialidad = ", BusEspecialidad )
    BusMedico = request.POST["busMedico"]
    BusServicio = request.POST["busServicio"]
    BusPaciente = request.POST["busPaciente"]
    Perfil = request.POST['Perfil']

    Sede = request.POST["Sede"]
    context['Sede'] = Sede

    # Consigo la sede Nombre

    miConexion = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    cur = miConexion.cursor()
    comando = "SELECT nombre   FROM sitios_sedesClinica WHERE id ='" + Sede + "'"
    cur.execute(comando)
    print(comando)

    nombreSedes = []

    for nombre in cur.fetchall():
        nombreSedes.append({'nombre': nombre})

    miConexion.close()
    print(nombreSedes)
    nombresede1 = nombreSedes[0]

    context['NombreSede'] = nombresede1


    Username = request.POST["Username"]
    context['Username'] = Username
    Username_id = request.POST["Username_id"]
    context['Username_id'] = Username_id




    print("Sede  = ", Sede)

    print("BusHabitacion= ", BusHabitacion)
    print("BusTipoDoc=", BusTipoDoc)
    print("BusDocumento=" , BusDocumento)
    print("BusDesde=", BusDesde)
    print("BusHasta=", BusHasta)
    print("La sede es = " , Sede)
    print("El busServicio = ", BusServicio)
    print("El busEspecialidad = ", BusEspecialidad)
    print("El busSMedico = ", BusMedico)
    print("El busSMedico = ", BusPaciente)

    ingresos = []

    # Combo de Servicios
    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
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
    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
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
    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM usuarios_TiposDocumento"
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
    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM sitios_dependencias where sedesClinica_id = '" + str(Sede) +"' AND dependenciasTipo_id = 2"
    curt.execute(comando)
    print(comando)

    habitaciones = []
    habitaciones.append({'id': '', 'nombre': ''})


    for id, nombre in curt.fetchall():
        habitaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(habitaciones)

    context['Habitaciones'] = habitaciones

    # Fin combo Habitaciones

    # Combo Especialidades
    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
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
    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    curt = miConexiont.cursor()
    comando = "SELECT p.id id, p.nombre  nombre FROM planta_planta p ,  planta_perfilesplanta perf WHERE p.sedesClinica_id = perf.sedesClinica_id and  perf.sedesClinica_id = '" + str(
        Sede) + "' AND perf.tiposPlanta_id = 1 and p.id = perf.planta_id"

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


    # Busco Nombre de Habitacion

    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    curt = miConexiont.cursor()
    comando = "SELECT d.id id, d.nombre  nombre FROM sitios_dependencias d WHERE d.id = '" + str(BusHabitacion) + "'"
    curt.execute(comando)
    print(comando)

    NombreHabitacion = ""


    for id, nombre in curt.fetchall():
        NombreHabitacion = nombre

    miConexiont.close()
    print("NombreHabitacion = ", NombreHabitacion)


    # Fin busco nombre de habitacion



    miConexion1 = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    cur1 = miConexion1.cursor()

 #   detalle = "SELECT i.tipoDoc_id tipoDoc, i.documento_id documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, serviciosIng_id,  dependenciasIngreso_id , dxIngreso_id FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep  WHERE i.sedesClinica_id = dep.sedesClinica_id AND i.dependenciasActual_id = dep.id AND i.sedesClinica_id = '" +    str(Sede) +"'"
  #  detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag  WHERE i.sedesClinica_id = dep.sedesClinica_id AND i.serviciosActual_id = dep.servicios_id AND i.serviciosActual_id = ser.id  AND i.dependenciasActual_id = dep.id AND  i.dependenciasIngreso_id = dep.id AND i.sedesClinica_id= '" + str(Sede) + "' AND dep.sedesClinica_id = i.sedesClinica_id AND i.sedesClinica_id = ser.sedesClinica_id AND deptip.id = dep.dependenciasTipo_id  AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and diag.id = i.dxactual_id"
    detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd.sedesClinica_id = i.sedesClinica_id  and   sd.servicios_id  = ser.id and   i.sedesClinica_id = dep.sedesClinica_id AND i.dependenciasActual_id = dep.id AND i.sedesClinica_id= '" + str(Sede) + "'  AND  deptip.id = dep.dependenciasTipo_id and dep.servicios_id = ser.id AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and u.id = i.documento_id and diag.id = i.dxactual_id"


    print(detalle)

    desdeTiempo = BusDesde[11:16]
    hastaTiempo = BusHasta[11:16]
    desdeFecha = BusDesde[0:10]
    hastaFecha = BusHasta[0:10]

    print ("desdeTiempo = ", desdeTiempo)
    print("desdeTiempo = " ,hastaTiempo)

    print (" desde fecha = " , desdeFecha)
    print("hasta "
          " = ", hastaFecha)


    if BusServicio != "":
      detalle = detalle + " AND  ser.id = '" + str(BusServicio) + "'"
    print(detalle)

    if BusDesde != "":
        detalle = detalle +  " AND i.fechaIngreso >= '" + str(desdeFecha) + " " + desdeTiempo + ":00'"
        print (detalle)

    if BusHasta != "":
        detalle = detalle + " AND i.fechaIngreso <=  '" + str(hastaFecha) + " " + hastaTiempo + ":00'"
        print(detalle)

    if BusHabitacion != "":
        detalle = detalle + " AND dep.id = '" + str(BusHabitacion) + "'"
        print(detalle)

    if BusTipoDoc != "":
            detalle = detalle + " AND i.tipoDoc_id= '" + str(BusTipoDoc) + "'"
            print(detalle)

    if BusDocumento != "":
                detalle = detalle + " AND u.documento= '" + str(BusDocumento) + "'"
                print(detalle)

    if BusPaciente != "":
        detalle = detalle + " AND u.nombre like '%" + str(BusPaciente) + "%'"
        print(detalle)

    if BusMedico != "":
        detalle = detalle + " AND i.medicoActual_id = '"  + str(BusMedico) + "'"
        print(detalle)


    if BusEspecialidad != "":
        detalle = detalle + " AND i.dxIngreso_id = '" + str(BusEspecialidad) + "'"
        print(detalle)




    cur1.execute(detalle)



    for tipoDoc, documento_id, nombre , consec, fechaIngreso,  fechaSalida, servicioNombreIng, camaNombreIng, dxActual  in cur1.fetchall():

        ingresos.append ({'tipoDoc' : tipoDoc, 'Documento': documento_id, 'Nombre': nombre , 'Consec': consec, 'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida, 'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng, 'DxActual': dxActual})

    miConexion1.close()
    print(ingresos)
    context['Ingresos'] = ingresos




    return render(request, "admisiones/panelAdmisiones.html", context)



def buscarSubServicios(request):
    context = {}
    Serv = request.GET["Serv"]
    Sede = request.GET["Sede"]
    print ("Entre buscar  servicio =",Serv)
    print ("Sede = ", Sede)

    # Combo de SubServicios
    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    curt = miConexiont.cursor()
    comando = "SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed.sedesClinica_id ='" + str(
        Sede) + "' AND sed.servicios_id = ser.id and  sed.sedesClinica_id = sub.sedesClinica_id and sed.servicios_id =sub.servicios_id and  sub.servicios_id = '" + str(Serv) + "'"
    curt.execute(comando)
    print(comando)

    subServicios = []
    subServicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        subServicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(subServicios)

    context['SubServicios'] = subServicios





    context['Sede'] = Sede



    return JsonResponse(json.dumps(subServicios), safe=False)



def buscarCiudades(request):
    context = {}
    Departamento = request.GET["Departamento"]

    print ("Entre buscar  Ciudades del Depto  =",Departamento)


    # Combo de Medicos Especialidades


    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    curt = miConexiont.cursor()

    comando = "SELECT c.id id, c.nombre  nombre FROM sitios_departamentos d, sitios_ciudades c WHERE c.departamentos_id = d.id and d.id = '" + str(Departamento) + "'"

    curt.execute(comando)
    print(comando)

    ciudades = []



    for id, nombre in curt.fetchall():
        ciudades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(ciudades)


    context['Ciudades'] = ciudades


    return JsonResponse(json.dumps(ciudades), safe=False)




def buscarEspecialidadesMedicos(request):
    context = {}
    Esp = request.GET["Esp"]
    Sede = request.GET["Sede"]
    print ("Entre buscar  Servicio =",Esp)
    print ("Sede = ", Sede)

    # Combo de Medicos Especialidades


    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    curt = miConexiont.cursor()

    comando = "SELECT p.id id, p.nombre  nombre FROM planta_planta p ,  planta_perfilesplanta perf  , clinico_especialidadesmedicos espmed WHERE p.sedesClinica_id = perf.sedesClinica_id and  perf.sedesClinica_id = '" + str(
        Sede) + "' AND perf.tiposPlanta_id = 1   and p.id = perf.planta_id  AND espmed.planta_id = p.id AND  espmed.especialidades_id = '" +str(Esp) + "'"

    curt.execute(comando)
    print(comando)

    medicosEspecialidades = []



    for id, nombre in curt.fetchall():
        medicosEspecialidades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(medicosEspecialidades)


    context['MedicosEspecialidades'] = medicosEspecialidades

    context['Sede'] = Sede



    return JsonResponse(json.dumps(medicosEspecialidades), safe=False)





def buscarHabitaciones(request):


    context = {}
    Exc = request.GET["Exc"]
    print ("Excluir = ", Exc)
    Serv = request.GET["Serv"]
    SubServ = request.GET["SubServ"]
    Sede = request.GET["Sede"]
    print ("Entre buscar  servicio =",Serv)
    print("Entre buscar Subservicio =", SubServ)
    print ("Sede = ", Sede)


    # Busco la habitaciones de un Servicio

    miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    curt = miConexiont.cursor()

    if Exc == 'N':

      comando = "SELECT dep.id id ,dep.numero nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub , sitios_dependencias dep  Where sed.sedesClinica_id ='" + str(
        Sede) + "' AND sed.servicios_id = ser.id and  sed.sedesClinica_id = sub.sedesClinica_id and sed.servicios_id =sub.servicios_id and  dep.sedesClinica_id=sed.sedesClinica_id and dep.servicios_id = sub.servicios_id and dep.subServicios_id =sub.id  and dep.subServicios_id = '" +str(SubServ) + "'"

    else:
        comando = "SELECT dep.id id ,dep.numero nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub , sitios_dependencias dep , sitios_dependenciasActual act   Where sed.sedesClinica_id ='" + str(
            Sede) + "' AND sed.servicios_id = ser.id and  sed.sedesClinica_id = sub.sedesClinica_id and sed.servicios_id =sub.servicios_id and  dep.sedesClinica_id=sed.sedesClinica_id and dep.servicios_id = sub.servicios_id and dep.subServicios_id =sub.id  and dep.subServicios_id = '" + str(
            SubServ) + "' and act.dependencias_id = dep.id and act.disponibilidad = 'L' UNION SELECT dep.id id ,dep.numero nombre FROM sitios_serviciosSedes sed, clinico_servicios ser , sitios_subserviciossedes sub , sitios_dependencias dep Where sed.sedesClinica_id ='" + str(Sede) + "'  AND sed.servicios_id = ser.id and sed.sedesClinica_id = sub.sedesClinica_id and sed.servicios_id =sub.servicios_id and dep.sedesClinica_id=sed.sedesClinica_id and dep.servicios_id = sub.servicios_id and dep.subServicios_id =sub.id and dep.subServicios_id = '" + str(SubServ) + "' and not EXISTS  (select act.id from sitios_dependenciasactual act where act.dependencias_id = dep.id)"


    curt.execute(comando)
    print(comando)

    Habitaciones =[]




    for id, nombre in curt.fetchall():
        Habitaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(Habitaciones)
    context['Habitaciones'] = Habitaciones

    context['Sede'] = Sede



    return JsonResponse(json.dumps(Habitaciones), safe=False)



# aqui nuevo codigo cvrear admision DEF


def crearAdmisionDef(request):

    print("Entre a Craer Admision definitiva")

    if request.method == 'POST':
        print("EntrePost Graba Admision Def")
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
        print(" Username = " , Username)
        context['Username'] = Username

        Username_id = request.POST["Username_id"]
        print("Username_id = ", Username_id)
        context['Username_id'] = Username_id



        tipoDoc = request.POST['tipoDoc']
       # documento = request.POST['documento']
        documento = request.POST['busDocumentoSel']
        print("tipoDoc = ", tipoDoc)
        print("documento = ", documento)
        #extraServicio = request.POST['extraServicio']
       #print("extraServicio = ", extraServicio)

        # Consigo el Id del Paciente Documento

        DocumentoId = Usuarios.objects.get(documento=documento)
        idPacienteFinal = DocumentoId.id

        print("idPacienteFinal", idPacienteFinal)



        consec = Ingresos.objects.all().filter(tipoDoc_id=tipoDoc).filter(documento_id=idPacienteFinal).aggregate(maximo=Coalesce(Max('consec'), 0))
        print("ultimo Ingreso = ", consec)
        consecAdmision = (consec['maximo'] + 1)
        print("ultimo ingreso = ", consecAdmision)

        fechaIngreso = request.POST['fechaIngreso']
        print("fechaIngreso =", fechaIngreso)

        fechaSalida = "0001-01-01 00:00:00"

        factura = 0
        numcita = 0
        dependenciasIngreso = request.POST['dependenciasIngreso']
        print("dependenciasIngreso =", dependenciasIngreso)
        dependenciasActual = dependenciasIngreso
        dependenciasSalida = ""
        dxIngreso = request.POST['dxIngreso']
        print("dxIngreso =", dxIngreso)
        dxActual = dxIngreso
        dxSalida = ""
        estadoSalida = "1"

        medicoIngreso = request.POST['medicoIngreso']
        print("medicoIngreso =", medicoIngreso)
        medicoActual = medicoIngreso
        medicoSalida = ""
        salidaClinica = "N"
        salidaDefinitiva = "N"

        especialidadesMedicos = request.POST['busEspecialidad']

        especialidadesMedicosSalida = ""
        especialidadesMedicosActual = especialidadesMedicos


        usuarioRegistro = Username_id

        print("usuarioRegistro =", usuarioRegistro)
        now = datetime.now()
        dnow=now.strftime("%Y-%m-%d %H:%M:%S")
        print ("NOW  = ", dnow)

        fechaRegistro = dnow
        estadoReg = "A"
        print("estadoRegistro =", estadoReg)

        data[0] = "Ha ocurrido un error"

        # VAmos a guardar la Admision

        # Consigo ID de Documento

        documento_llave = Usuarios.objects.get(documento=documento)
        print("el id del dopcumento = ", documento_llave.id)

        grabo = Ingresos(
                         sedesClinica_id=Sede,
                         tipoDoc_id=tipoDoc,
                         documento_id=documento_llave.id,
                         consec=consecAdmision,
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
        print("Voy a fiu¿guardar la INFO")

        grabo.save()
        print("yA grabe 2", grabo.id)
        grabo.id
        print("yA grabe" , grabo.id)

        # Grabo Dependencia Historico

        print("Voy a guardar HISTORICO dependencias ")

        grabo2 = HistorialDependencias(
            tipoDoc_id=tipoDoc,
            documento_id=documento_llave.id,
            consec=consecAdmision,
            dependencias_id=dependenciasIngreso,
            fechaOcupacion=fechaRegistro,
            fechaLiberacion=fechaSalida,
            fechaRegistro=fechaRegistro,
            usuarioRegistro_id=usuarioRegistro,
            estadoReg=estadoReg

        )
        grabo2.save()

        print("Grabe HISTPRICO DEPENDENCIAS")

        # Averiguar si ya hay una Dependencia Actual creada o actualizarla

        miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
        curt = miConexiont.cursor()
        comando = "SELECT id ,disponibilidad nombre FROM sitios_dependenciasActual WHERE dependencias_id = '" + str(dependenciasIngreso) + "'"
        curt.execute(comando)
        print(comando)

        dependenciasActual = []

        for id, nombre in curt.fetchall():
            dependenciasActual.append({'id': id, 'nombre': nombre})

        miConexiont.close()


        if dependenciasActual != []:

            print("Voy a actualizar disponibilidad dependencias Actual")

            # Actualizo Disponibilidad de dependencia
            miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
            curt = miConexiont.cursor()
            comando = "UPDATE sitios_dependenciasActual  SET disponibilidad = 'O' WHERE dependencias_id = '" + str(dependenciasIngreso) + "'"
            curt.execute(comando)
            print(comando)
            miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
            curt = miConexiont.cursor()
            comando = "SELECT id ,disponibilidad nombre FROM sitios_dependenciasActual WHERE dependencias_id = '" + str(
                dependenciasIngreso) + "'"
            curt.execute(comando)
            print(comando)

            dependenciasActual = []

            for id, nombre in curt.fetchall():
                dependenciasActual.append({'id': id, 'nombre': nombre})

            miConexiont.commit
            miConexiont.close()


        else:

          # Grabo Dependencia Actual

          print("Voy a guardar dependencias Actual")

          grabo3 = DependenciasActual(
            tipoDoc_id=tipoDoc,
            documento_id=documento_llave.id,
            consec=consecAdmision,
            dependencias_id=dependenciasIngreso,
            disponibilidad='O',
            fecha=fechaRegistro,
            fechaRegistro=fechaRegistro,
            usuarioRegistro_id=usuarioRegistro,
            estadoReg=estadoReg
          )
          grabo3.save()

          print("GUARDADO dependencias Actual")



        # RUTINA ARMADO CONTEXT

        ingresos = []

        miConexionx = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
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
        miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
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
        miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
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
        miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
        curt = miConexiont.cursor()
        comando = "SELECT id ,nombre FROM usuarios_TiposDocumento "
        curt.execute(comando)
        print(comando)

        tiposDoc = []
        #tiposDoc.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposDoc.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposDoc)

        context['TiposDoc'] = tiposDoc

        # Fin combo TiposDOc

        # Combo Habitaciones
        miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
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
        miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
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
        miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
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

        # Combo TiposUsuario

        miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposusuario p"

        curt.execute(comando)
        print(comando)

        tiposUsuario = []
        # tiposUsuario.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposUsuario.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposUsuario)

        context['TiposUsuario'] = tiposUsuario

        # Fin combo Tipos Usuario

        # Combo TiposDocumento

        miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposDocumento p"

        curt.execute(comando)
        print(comando)

        tiposDocumento = []
        #tiposDocumento.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposDocumento.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposDocumento)

        context['TiposDocumento'] = tiposDocumento

        # Fin combo TiposDocumento

        # Combo Centros

        miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM sitios_centros p"

        curt.execute(comando)
        print(comando)

        centros = []

        for id, nombre in curt.fetchall():
            centros.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposDocumento)

        context['Centros'] = centros

        # Fin combo Centros

        # Combo Diagnosticos

        miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM clinico_diagnosticos p"

        curt.execute(comando)
        print(comando)

        diagnosticos = []
        diagnosticos.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            diagnosticos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(diagnosticos)

        context['Diagnosticos'] = diagnosticos

        # Fin combo Diagnosticos

        # FIN RUTINA ARMADO CONTEXT


    return render(request, "admisiones/panelAdmisiones.html", context)



# fin nuevo mcodigo crear admison DEF



def crearResponsables(request):
    print("Entre crear Responsables")
    pass


def UsuariosModal(request):
        print("Entre a Modal Usuario")

        tipoDoc = request.POST['tipoDoc']
        documento = request.POST['documento']

        print (documento)
        print(tipoDoc)

        #documento='19465673'
        #tipoDoc='1'

        miConexiont = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
        curt = miConexiont.cursor()
        comando = "SELECT nombre, documento, genero, departamentos_id, ciudades_id, direccion, telefono, contacto, centrosc_id, tipoDoc_id, tiposUsuario_id FROM usuarios_usuarios WHERE tipoDoc_id = " + str(tipoDoc) + " AND documento = " + str(documento) + ""
        print(comando)
        curt.execute(comando)

        Usuarios = {}

        for nombre, documento, genero, departamentos_id, ciudades_id, direccion, telefono, contacto, centrosc_id, tipoDoc_id, tiposUsuario_id  in curt.fetchall():
            Usuarios = {'nombre': nombre, 'documento': documento, 'genero': genero,'departamento' : departamentos_id, 'ciudad': ciudades_id,  'direccion':  direccion, 'telefono' :telefono, 'contacto': contacto, 'centrosc_id':centrosc_id, 'tipoDoc_id':tipoDoc_id,'tiposUsuario_id':tiposUsuario_id}

        miConexiont.close()
        print(Usuarios)

        if Usuarios == '[]':
            datos = {'Mensaje' : 'Usuario No existe'}
            return JsonResponse(datos, safe=False)
        else:
            return JsonResponse(Usuarios, safe=False)




def guardarUsuariosModal(request):
    print("Entre a grabar Usuarios")
    tipoDoc_id = request.POST["tipoDoc"]

    documento = request.POST["documento"]
    nombre = request.POST["nombre"]
    print(documento)
    print(nombre)
    genero = request.POST["genero"]
    departamento = request.POST["departamentos"]
    ciudad = request.POST["ciudades"]
    print ("departamento = ", departamento)
    print("ciudad = ", ciudad)

    direccion = request.POST["direccion"]
    telefono = request.POST["telefono"]
    contacto = request.POST["contacto"]
    centrosc_id = request.POST["centrosc"]
    tiposUsuario_id = request.POST["tiposUsuario"]

    print(documento)
    print(tipoDoc_id)

    miConexion11 =  MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
    cur11 = miConexion11.cursor()
    comando = "SELECT id, tipoDoc_id, documento FROM usuarios_usuarios WHERE tipoDoc_id = '" + str(tipoDoc_id) + "' AND documento = '" + str(documento) + "'"
    print(comando)
    cur11.execute(comando)

    Usuarios = []

    for id, tipoDoc_id, documento in cur11.fetchall():
        Usuarios.append({'id': id, 'tipoDoc_id': tipoDoc_id, 'documento': documento})

    miConexion11.close()

    if Usuarios == []:

         print("Entre a crear")
         miConexion3 = MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
         cur3 = miConexion3.cursor()
         comando = "insert into usuarios_usuarios (nombre, documento, genero, departamentos_id, ciudades_id, direccion, telefono, contacto, centrosc_id, tipoDoc_id, tiposUsuario_id) values ('" + nombre + "' , '" + documento + "', '" + genero + "'  , '" + departamento +  "'  , '" +  ciudad + "'  , '" +  direccion + "', '" + telefono + "', '" + contacto + "', '" + centrosc_id +  "', '" + tipoDoc_id + "', '" + tiposUsuario_id + "')"
         print(comando)
         cur3.execute(comando)
         miConexion3.commit()
         miConexion3.close()
         return HttpResponse("Usuario Creado ! ")
    else:
        print("Entre a actualizar")
        miConexion3 =  MySQLdb.connect(host='localhost', user='root', passwd='', db='vulnerable9')
        cur3 = miConexion3.cursor()
        comando = "update usuarios_usuarios set nombre = '" + nombre +   "', direccion  = '" + direccion  + "', genero = '" + genero  + "', telefono= '" + telefono + "', contacto= '" + contacto + "', centrosc_id= '" + centrosc_id + "', tiposUsuario_id = '" + tiposUsuario_id + "'     WHERE tipoDoc_id = '" + str(tipoDoc_id) + "' AND documento = '" + str(documento) + "'"
        print(comando)
        cur3.execute(comando)
        miConexion3.commit()


        miConexion3.close()
        return HttpResponse("Usuario Actualizado ! ")

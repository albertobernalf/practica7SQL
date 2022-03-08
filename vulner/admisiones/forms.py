from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import django.core.validators
import django.core.exceptions
from django.core.exceptions import ValidationError

from admisiones.models import Ingresos
from usuarios.models import TiposDocumento
from sitios.models import SedesClinica, Dependencias
from clinico.models import Diagnosticos, EstadosSalida, Servicios, Especialidades
from planta.models import Planta
import django.core.validators
import django.core.exceptions
from django.core.exceptions import ValidationError

import datetime


class crearAdmisionForm(forms.ModelForm):
    extraServicio = forms.ModelChoiceField(queryset=Servicios.objects.filter(id__lt=3))

    def save(self, commit=True):
        extraServicio = self.cleaned_data.get('extraServicio', None)
        # ...do something with extra_field here...
        return super(crearAdmisionForm, self).save(commit=commit)

    class Meta:
        model = Ingresos

        CHOICES = [('1', 'First'), ('2', 'Second')]
        sedesClinica = forms.ModelChoiceField(queryset=SedesClinica.objects.all())
        tipoDoc = forms.ModelChoiceField(queryset=TiposDocumento.objects.all() , required=True)
        documento = forms.IntegerField(label='No Documento' , required=True)
        consec = forms.IntegerField(label='Ingreso No', disabled=True)
        fechaIngreso = forms.DateTimeField(label="Fec.Ingreso : ", initial=datetime.date.today , required=True)
        fechaSalida = forms.DateTimeField(label="Fec.Salida : ", initial=datetime.date.today)
        factura = forms.IntegerField(initial=0, disabled=True)
        numcita = forms.IntegerField(initial=0, disabled=True)
        dependenciasIngreso = forms.ModelChoiceField(label="Dep.Ingreso : ", required=True, queryset=Dependencias.objects.all())
        dependenciasActual = forms.ModelChoiceField(label="Dep.Actual : ", queryset=Dependencias.objects.all())
        dependenciasSalida = forms.ModelChoiceField(label="Dep.Salida : ", queryset=Dependencias.objects.all())
        dxIngreso = forms.ModelChoiceField(label="Dx.Ingreso : ", required=True, queryset=Diagnosticos.objects.all())
        dxActual = forms.ModelChoiceField(label="Dx.Actual : ", queryset=Diagnosticos.objects.all())
        dxSalida = forms.ModelChoiceField(label="Dx.Salida : ", queryset=Diagnosticos.objects.all())
        estadoSalida = forms.ModelChoiceField(label="Estado Salida : ", queryset=EstadosSalida.objects.all())
        medicoIngreso = forms.ModelChoiceField(label="Med.Ingreso : ", required=True, queryset=Planta.objects.all())
        medicoActual = forms.ModelChoiceField(label="Med Actual : ", queryset=Planta.objects.all())
        medicoSalida = forms.ModelChoiceField(label="Med.Salida : ", queryset=Planta.objects.all())
        especialidadesMedicosIngreso = forms.ModelChoiceField(label="Esp Actual : ", required=True,
                                                              queryset=Especialidades.objects.all())
        especialidadesMedicosActual = forms.ModelChoiceField(label="Esp Actual : ",
                                                             queryset=Especialidades.objects.all())
        especialidadesMedicosSalida = forms.ModelChoiceField(label="Esp Actual : ",
                                                             queryset=Especialidades.objects.all())

        salidaDefinitiva = forms.CharField(label='Salida Definitiva', initial='N', max_length=1)
        usuarioRegistro = forms.CharField(label='SUsuario Registra', initial='N')
        fechaRegistro = forms.CharField(label='Fecha Registro', disabled=True)
        estadoRegistro = forms.CharField(label='Estado Registro', disabled=True, initial='A', max_length=1)

        fields = '__all__'

        widgets = {
            'tipoDoc_id': forms.TextInput(attrs={'class': 'form-group', 'placeholder': "tipoDoc"}),
            'documento_id': forms.TextInput(attrs={'class': 'form-group', 'placeholder': "Documento"}),
            'consec': forms.TextInput(attrs={'class': 'form-group', 'placeholder': "Consecutivo"}),
            # 'fechaIngreso' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Motivo"}),

            'fechaIngreso': forms.DateTimeInput(attrs={'class': 'form-group datetimepicker-input'}),
            'fechaSalida': forms.TextInput(attrs={'class': 'form-group', 'placeholder': "salida"}),

            'factura': forms.TextInput(attrs={'readonly': 'readonly'}),

            'numcita': forms.TextInput(attrs={'readonly': 'readonly'})
        }


    def clean_dxIngreso(self):
        print("Entre a validar diagnostico de imngreso")
        dxIngreso = self.cleaned_data.get('dxIngreso')
        print(dxIngreso)

        if dxIngreso != '':
            print("ok Diagnostico")
        else:
            raise forms.ValidationError('Suministre Diagnostico de Ingreso . ')

        return dxIngreso

    def clean_medicoIngreso(self):
        print("Entre a validar  de medicoIngreso")
        medicoIngreso = self.cleaned_data.get('medicoIngreso')
        print(medicoIngreso)

        if medicoIngreso != '':
            print("ok Medico")
        else:
            raise forms.ValidationError('Suministre medicoIngreso . ')

        return medicoIngreso
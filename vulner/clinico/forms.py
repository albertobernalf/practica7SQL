from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Historia, Especialidades, Medicos
from usuarios.models import TiposDocumento, Usuarios
from clinico.models import TiposExamen, Examenes, HistoriaExamenes,HistoriaExamenesCabezote, TiposFolio, CausasExterna, TiposIncapacidad, Incapacidades, Diagnosticos, HistorialDiagnosticosCabezote
from sitios.models import Dependencias
from planta.models import Planta
import django.core.validators
import django.core.exceptions
from django.core.exceptions import ValidationError


class IncapacidadesForm(forms.ModelForm):

    class Meta:
        model = Incapacidades

        tipoDoc = forms.IntegerField(label="Tipo Doc")
        documento = forms.CharField(label = "Documento")
        consecAdmision = forms.IntegerField(label="Consecuito de Ingreso")
        dependenciasRealizado = forms.ModelChoiceField(queryset=Dependencias.objects.all())
        folio = forms.IntegerField(label="Folio No" )
        fecha = forms.DateTimeField()
        tiposIncapacidad = forms.ModelChoiceField(queryset=TiposIncapacidad.objects.all())
        desdeFecha = forms.DateTimeField()
        hastaFecha = forms.DateTimeField()
        diagnosticos = forms.ModelChoiceField(queryset=Diagnosticos.objects.all())
        estadoReg = forms .CharField(max_length=1)

        fields = '__all__'


class HistorialDiagnosticosCabezoteForm(forms.ModelForm):

    class Meta:
        model = HistorialDiagnosticosCabezote

        tipoDoc = forms.IntegerField(label='Tipo Doc')
        documento = forms.IntegerField(label='No Documento')
        consecAdmision= forms.IntegerField(label='Admision No', disabled=True, initial=0)
        folio = forms.IntegerField(label='No Folio', disabled=True, initial=0)
        observaciones = forms.CharField(max_length=200)
        estadoReg = forms.CharField(max_length=1)

        fields = '__all__'

        widgets = {
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'width': "100%", 'cols': "40", 'rows': "4",
                                                   'placeholder': "Observaciones"})
        }



class HistoriaExamenesCabezoteForm(forms.ModelForm):


    class Meta:
        model = HistoriaExamenesCabezote

        historia = forms.IntegerField(label='Historia')
        #tipoDoc = forms.IntegerField(label='Tipo Doc')
        #documento = forms.IntegerField(label='No Documento')
        #consecAdmision = forms.IntegerField(label='Admision No', disabled=True, initial=0)
        #folio = forms.IntegerField(label='No Folio', disabled=True, initial=0)
        observaciones =forms.CharField(max_length=200)
        tiposExamen = forms.ModelChoiceField(queryset=TiposExamen.objects.all())
        #fechaRegistro = forms.DateTimeField()
        #usuarioRegistro = forms.IntegerField(label='Usuario Documento')
        estadoReg = forms.CharField(max_length=1)

        fields = '__all__'

        widgets = {
            'observaciones': forms.Textarea(
                attrs={'class': 'form-control', 'width': "100%", 'cols': "40", 'rows': "4", 'placeholder': "Observaciones"})
        }



class historiaForm(forms.ModelForm):

    class Meta:
        model = Historia

        tipoDoc = forms.ModelChoiceField(queryset=TiposDocumento.objects.all())
        documento = forms.IntegerField(label='No Documento')
        consecAdmision = forms.IntegerField(label='Admision No', disabled=True, initial=0)
        folio = forms.IntegerField(label='No Folio', disabled=True, initial=0)
        fecha = forms.DateTimeField()

        tiposFolio = forms.ModelChoiceField(queryset=TiposFolio.objects.all())
        causasExterna = forms.ModelChoiceField(queryset=CausasExterna.objects.all())
        dependenciasRealizado = forms.ModelChoiceField(queryset=Dependencias.objects.all())
        especialidades = forms.ModelChoiceField(queryset=Especialidades.objects.all())
        planta = forms.ModelChoiceField(queryset=Planta.objects.all())

        fechaRegistro =  forms.DateTimeField()
        usuarioRegistro = forms.ModelChoiceField(queryset=Usuarios.objects.all())

        fields = '__all__'

        widgets = {
            'motivo':    forms.Textarea(attrs={'class': 'form-control', 'width': "100%", 'cols': "40", 'rows': "4", 'placeholder': "Motivo"}),
            'subjetivo': forms.Textarea(attrs={'class': 'form-control', 'width': "100%", 'cols': "40", 'rows': "4", 'placeholder': "Subjetivo"}),
            'objetivo':  forms.Textarea(attrs={'class': 'form-control', 'width': "100%", 'cols': "40", 'rows': "4", 'placeholder': "Objetivo"}),
            'analisis':  forms.Textarea(attrs={'class': 'form-control', 'width': "100%", 'cols': "40", 'rows': "4", 'placeholder': "Analisis"}),
            'plan':      forms.Textarea(attrs={'class': 'form-control', 'width': "100%", 'cols': "40", 'rows': "4", 'placeholder': "Plan"}),
            'folio':     forms.TextInput(attrs={'readonly': 'readonly'})
        }


    def clean_documento(self):
        print("entre a validar Documento Historia1 Form")
        documento = self.cleaned_data.get('documento')
        print (documento)
        id_tipo_doc = self.cleaned_data.get('id_tipo_doc')
        print(id_tipo_doc)
        id_tipo_doc1 = TiposDocumento.objects.get(nombre=id_tipo_doc)
        print(id_tipo_doc1.id)
        if Usuarios.objects.all().filter(id_tipo_doc=id_tipo_doc1.id).filter(nombre=documento).exists():
            print("ok Documento")
        else:
            raise forms.ValidationError('Documento de Usuario No existe . ')
            return documento
        return documento

    def clean_fecha(self):
        print("Entre Historia1View validar Fecha")
        fecha = self.cleaned_data.get('fecha')
        print(fecha)

        return fecha


    def clean_motivo(self):
        print("Entre Historia1View validar motivo")
        motivo = self.cleaned_data.get('motivo')
        print(motivo)

        return motivo






class historiaExamenesForm(forms.ModelForm):

    class Meta:
        model = HistoriaExamenes

        id_tipo_doc = forms.ModelChoiceField(queryset=TiposDocumento.objects.all())
        documento = forms.IntegerField(label='No Documento')
        folio = forms.IntegerField(label='No Folio', disabled=True, initial=0)
        fecha = forms.DateTimeField()
        id_TipoExamen = forms.ModelChoiceField(queryset=TiposExamen.objects.all())
        id_examen = forms.ModelChoiceField(queryset=Examenes.objects.all())
        cantidad = forms.IntegerField(label='Cantidad')

        estado_folio = forms.CharField(label='Estado del Folio', disabled=True, initial='A', max_length=1)

        fields = '__all__'

    def clean_fecha(self):
        print ("Entre Fecha")
        fecha = self.cleaned_data.get('fecha')
        print(fecha)

        return fecha

    def clean_cantidad(self):
            print("Entre cantidad")
            cantidad = self.cleaned_data.get('cantidad')
            print(cantidad)

            return cantidad

    def clean_estado_folio(self):
        print("Entre esadofoklio")
        estado_folio = self.cleaned_data.get('estado_folio')
        print(estado_folio)

        return estado_folio


    def clean_id_examen(self):
        print("Entre id_examen")
        id_examen = self.cleaned_data.get('id_examen')
        print(id_examen)

        return id_examen

    def clean_id_TipoExamen(self):
        print("Entre id_TipoExamen")
        id_TipoExamen = self.cleaned_data.get('id_TipoExamen')
        print(id_TipoExamen)

        return id_TipoExamen








# Generated by Django 3.2 on 2022-03-07 19:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clinico', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Centros',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('ubicacion', models.CharField(default='', max_length=50)),
                ('direccion', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=20)),
                ('contacto', models.CharField(max_length=50)),
                ('fechaRegistro', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('estadoReg', models.CharField(default='A', editable=False, max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Ciudades',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('fechaRegistro', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('estadoReg', models.CharField(default='A', editable=False, max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Departamentos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('fechaRegistro', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('estadoReg', models.CharField(default='A', editable=False, max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Dependencias',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('numero', models.CharField(default='', max_length=50)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=50)),
                ('fechaRegistro', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('estadoReg', models.CharField(default='A', editable=False, max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='DependenciasActual',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('consec', models.IntegerField()),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('disponibilidad', models.CharField(choices=[('L', 'LIBRE'), ('O', 'OCUPADA')], default='L', max_length=1)),
                ('fechaRegistro', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('estadoReg', models.CharField(default='A', editable=False, max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='DependenciasTipo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SedesClinica',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('ubicacion', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=20)),
                ('contacto', models.CharField(max_length=50)),
                ('fechaRegistro', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('estadoReg', models.CharField(default='A', editable=False, max_length=1)),
                ('ciudades', smart_selects.db_fields.ChainedForeignKey(chained_field='departamentos', chained_model_field='departamentos', on_delete=django.db.models.deletion.CASCADE, to='sitios.ciudades')),
                ('departamentos', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='sitios.departamentos')),
            ],
        ),
        migrations.CreateModel(
            name='ServiciosSedes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=50)),
                ('estadoReg', models.CharField(default='A', editable=False, max_length=1)),
                ('sedesClinica', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='sitios.sedesclinica')),
                ('servicios', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='clinico.servicios')),
            ],
        ),
        migrations.CreateModel(
            name='SubServiciosSedes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subServicios', models.CharField(default='', max_length=50)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=50)),
                ('estadoReg', models.CharField(default='A', editable=False, max_length=1)),
                ('sedesClinica', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='sitios.sedesclinica')),
                ('servicios', smart_selects.db_fields.ChainedForeignKey(chained_field='sedesClinica', chained_model_field='sedesClinica', on_delete=django.db.models.deletion.CASCADE, to='sitios.serviciossedes')),
            ],
        ),
        migrations.CreateModel(
            name='HistorialDependencias',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('consec', models.IntegerField()),
                ('fechaOcupacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fechaLiberacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fechaRegistro', models.DateTimeField(default=django.utils.timezone.now)),
                ('estadoReg', models.CharField(default='A', editable=False, max_length=1)),
                ('dependencias', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='sitios.dependencias')),
            ],
        ),
    ]

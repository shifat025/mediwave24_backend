# Generated by Django 5.1.1 on 2024-09-16 16:49

import autoslug.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_doctor_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='available_time',
        ),
        migrations.RemoveField(
            model_name='specialization',
            name='user',
        ),
        migrations.AddField(
            model_name='specialization',
            name='certification_type',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='specialization',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor'),
        ),
        migrations.AddField(
            model_name='specialization',
            name='document',
            field=models.ImageField(blank=True, null=True, upload_to='doctor/media/uploads'),
        ),
        migrations.CreateModel(
            name='AvailableTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=50)),
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('doctor', models.ManyToManyField(to='doctor.doctor')),
            ],
        ),
        migrations.AddField(
            model_name='specialization',
            name='specializanation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='doctor.department'),
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hosspital_name', models.CharField(max_length=50)),
                ('designation', models.CharField(max_length=30)),
                ('department', models.CharField(max_length=30)),
                ('employee_period_start', models.DateField()),
                ('employee_period_end', models.DateField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regular_fee', models.CharField(max_length=30)),
                ('folowup_fee', models.CharField(blank=True, max_length=30, null=True)),
                ('discount_fee', models.CharField(blank=True, max_length=30, null=True)),
                ('free', models.BooleanField(default=False)),
                ('discount', models.BooleanField(default=False)),
                ('followup', models.BooleanField(default=False)),
                ('consultation_duration', models.CharField(max_length=30)),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='NationID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='doctor/media/uploads')),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='ProfessionalQualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree_name', models.CharField(max_length=30)),
                ('institue_name', models.CharField(max_length=50)),
                ('institue_location', models.CharField(max_length=50)),
                ('passing_year', models.DateField()),
                ('duration', models.CharField(max_length=10)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='doctor/media/uploads')),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor')),
            ],
        ),
        migrations.DeleteModel(
            name='Designation',
        ),
    ]

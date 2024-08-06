# Generated by Django 4.2.14 on 2024-08-06 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FETCH', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cropdetails',
            fields=[
                ('unique_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('area_cultivated', models.IntegerField(blank=True, null=True)),
                ('crop_type', models.CharField(blank=True, max_length=100, null=True)),
                ('yeild_perhectare', models.IntegerField(blank=True, null=True)),
                ('soil_type', models.CharField(blank=True, max_length=50, null=True)),
                ('irrigation_method', models.CharField(blank=True, max_length=100, null=True)),
                ('temp_min', models.IntegerField(blank=True, null=True)),
                ('temp_max', models.IntegerField(blank=True, null=True)),
                ('temp_avg', models.IntegerField(blank=True, null=True)),
                ('rainfall_total', models.IntegerField(blank=True, null=True)),
                ('rainfall_rainy_days', models.IntegerField(blank=True, null=True)),
                ('humidity', models.IntegerField(blank=True, null=True)),
                ('fertilizer_NPK_kg', models.IntegerField(blank=True, null=True)),
                ('fertilizer_COMPOST_kg', models.IntegerField(blank=True, null=True)),
                ('pesticide_type', models.CharField(blank=True, max_length=100, null=True)),
                ('pesticide_quantity_l', models.IntegerField(blank=True, null=True)),
                ('district', models.ForeignKey(blank=True, default=480, null=True, on_delete=django.db.models.deletion.CASCADE, to='FETCH.district')),
                ('state', models.ForeignKey(blank=True, default=27, null=True, on_delete=django.db.models.deletion.CASCADE, to='FETCH.state')),
                ('subdistrict', models.ForeignKey(blank=True, default=3648, null=True, on_delete=django.db.models.deletion.CASCADE, to='FETCH.subdistrict')),
                ('village', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='FETCH.village')),
            ],
        ),
    ]

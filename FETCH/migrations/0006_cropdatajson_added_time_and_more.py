# Generated by Django 4.2.14 on 2024-08-12 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FETCH', '0005_cropdatajson_process_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cropdatajson',
            name='added_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cropdatajson',
            name='process_id',
            field=models.CharField(blank=True, null=True),
        ),
    ]
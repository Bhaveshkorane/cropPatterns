# Generated by Django 4.2.14 on 2024-08-02 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FETCH', '0004_cropdata_subdistrict'),
    ]

    operations = [
        migrations.AddField(
            model_name='cropdatajson',
            name='added',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]

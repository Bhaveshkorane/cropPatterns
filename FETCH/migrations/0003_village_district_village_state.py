# Generated by Django 4.2.14 on 2024-07-24 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FETCH', '0002_subdistrict_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='village',
            name='district',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='village',
            name='state',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]

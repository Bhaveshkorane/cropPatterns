# Generated by Django 4.2.14 on 2024-07-24 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FETCH', '0006_rename_vilagecreated_village_villagecreated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='village',
            name='district',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='FETCH.district'),
        ),
        migrations.AlterField(
            model_name='village',
            name='state',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='FETCH.state'),
        ),
    ]
# Generated by Django 5.1.5 on 2025-02-26 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disciplinas', '0009_notascornell_notascornellsumario_notascornelltopico_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notascornell',
            name='sumario',
            field=models.CharField(null=True),
        ),
        migrations.DeleteModel(
            name='NotasCornellSumario',
        ),
    ]

# Generated by Django 5.1.5 on 2025-02-26 03:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disciplinas', '0008_alter_mapastextos_aula'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotasCornell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='disciplinas.aulas')),
            ],
        ),
        migrations.CreateModel(
            name='NotasCornellSumario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sumario', models.CharField()),
                ('nota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='disciplinas.notascornell')),
            ],
        ),
        migrations.CreateModel(
            name='NotasCornellTopico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topico', models.CharField()),
                ('cor', models.CharField()),
                ('nota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='disciplinas.notascornell')),
            ],
        ),
        migrations.CreateModel(
            name='NotasCornellAnotacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anotacao', models.CharField()),
                ('nota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='disciplinas.notascornell')),
                ('topico', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='disciplinas.notascornelltopico')),
            ],
        ),
    ]

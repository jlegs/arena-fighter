# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-16 04:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arenafighter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialArmorItemProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default=b'')),
            ],
        ),
        migrations.CreateModel(
            name='SpecialWeaponItemProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default=b'')),
            ],
        ),
        migrations.AlterField(
            model_name='character',
            name='hpmax',
            field=models.IntegerField(default=47),
        ),
        migrations.AlterField(
            model_name='enemy',
            name='gold',
            field=models.IntegerField(default=17),
        ),
        migrations.AddField(
            model_name='armor',
            name='special_property',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='armors', to='arenafighter.SpecialArmorItemProperty'),
        ),
        migrations.AddField(
            model_name='weapon',
            name='special_property',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weapons', to='arenafighter.SpecialWeaponItemProperty'),
        ),
    ]

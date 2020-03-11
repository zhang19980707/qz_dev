# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booktest', '0002_auto_20171104_0817'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('atitle', models.CharField(max_length=20)),
                ('aParent', models.ForeignKey(null=True, to='booktest.AreaInfo', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='heroinfo',
            name='hcomment',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

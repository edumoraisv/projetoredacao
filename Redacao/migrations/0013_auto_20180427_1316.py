# Generated by Django 2.0.4 on 2018-04-27 13:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Redacao', '0012_auto_20180427_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redacao',
            name='data_pedido',
            field=models.DateTimeField(default=datetime.datetime.now, null=True),
        ),
    ]
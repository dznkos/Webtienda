# Generated by Django 2.0.13 on 2019-04-11 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0004_carritocompras'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carritocompras',
            name='precio',
            field=models.IntegerField(),
        ),
    ]

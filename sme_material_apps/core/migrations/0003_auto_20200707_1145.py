# Generated by Django 2.2.9 on 2020-07-07 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_material'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='material',
            options={'verbose_name': 'Item de Material', 'verbose_name_plural': 'Itens de Materiais'},
        ),
    ]

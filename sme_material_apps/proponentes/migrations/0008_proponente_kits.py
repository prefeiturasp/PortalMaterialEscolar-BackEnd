# Generated by Django 2.2.9 on 2020-07-29 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_kit_preco_maximo'),
        ('proponentes', '0007_auto_20200724_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='proponente',
            name='kits',
            field=models.ManyToManyField(blank=True, null=True, related_name='proponentes', to='core.Kit'),
        ),
    ]
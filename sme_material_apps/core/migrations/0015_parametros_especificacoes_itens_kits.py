# Generated by Django 2.2.9 on 2021-03-10 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20200804_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametros',
            name='especificacoes_itens_kits',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Especificações de itens dos kits'),
        ),
    ]

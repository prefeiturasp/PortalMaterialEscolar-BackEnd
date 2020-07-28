# Generated by Django 2.2.9 on 2020-07-24 15:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_kits'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialKit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('unidades', models.PositiveSmallIntegerField(default=1)),
                ('kit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materiais_do_kit', to='core.Kits')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kit_do_material', to='core.Material')),
            ],
            options={
                'verbose_name': 'Material do Kit',
                'verbose_name_plural': 'Materiais dos Kits',
            },
        ),
    ]

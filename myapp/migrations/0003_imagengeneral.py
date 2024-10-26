# Generated by Django 5.1.2 on 2024-10-25 16:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imagengeneral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('imagen', models.ImageField(upload_to='imagenes/')),
                ('tipo', models.CharField(choices=[('ai', 'ai'), ('human', 'human')], max_length=10)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.usuario')),
            ],
        ),
    ]

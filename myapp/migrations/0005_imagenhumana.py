# Generated by Django 5.1.2 on 2024-10-25 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_imagenia'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagenHumana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('imagen', models.ImageField(upload_to='human/')),
            ],
        ),
    ]

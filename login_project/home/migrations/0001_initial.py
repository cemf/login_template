# Generated by Django 5.1.7 on 2025-04-25 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=100)),
                ('login', models.CharField(max_length=50, unique=True)),
                ('senha', models.CharField(max_length=100)),
                ('endereco', models.TextField()),
            ],
        ),
    ]

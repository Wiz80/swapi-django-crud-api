# Generated by Django 4.2.15 on 2024-08-19 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('population', models.CharField(blank=True, max_length=100, null=True)),
                ('terrains', models.CharField(max_length=255)),
                ('climates', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddConstraint(
            model_name='planet',
            constraint=models.UniqueConstraint(fields=('name', 'population', 'terrains', 'climates'), name='unique_planets_values'),
        ),
    ]

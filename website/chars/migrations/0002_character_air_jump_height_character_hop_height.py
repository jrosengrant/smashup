# Generated by Django 5.0.4 on 2024-04-30 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chars', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='air_jump_height',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='air jump height'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='character',
            name='hop_height',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='shorthop height'),
            preserve_default=False,
        ),
    ]

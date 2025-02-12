# Generated by Django 4.2.18 on 2025-01-22 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_district_options_alter_state_options_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='district',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='state',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]

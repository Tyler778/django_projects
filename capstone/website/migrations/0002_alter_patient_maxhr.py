# Generated by Django 3.2.12 on 2022-02-14 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='maxHR',
            field=models.IntegerField(help_text='Enter the max heart rate of the patient'),
        ),
    ]
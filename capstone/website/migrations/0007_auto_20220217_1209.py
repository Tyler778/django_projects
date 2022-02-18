# Generated by Django 3.2.12 on 2022-02-17 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20220215_0930'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visualization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='patient',
            name='fastingBS',
            field=models.CharField(choices=[('1', 'Above 120mg/dl'), ('0', 'Less than 120mb/dl')], help_text='Enter fasting blood sugar of patient', max_length=3),
        ),
    ]
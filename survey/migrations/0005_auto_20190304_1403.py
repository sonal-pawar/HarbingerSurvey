# Generated by Django 2.1.7 on 2019-03-04 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_auto_20190304_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyemployee',
            name='endDatetime',
            field=models.DateTimeField(verbose_name='DD-MM-YYYY'),
        ),
        migrations.AlterField(
            model_name='surveyemployee',
            name='startDatetime',
            field=models.DateTimeField(verbose_name='DD-MM-YYYY'),
        ),
    ]
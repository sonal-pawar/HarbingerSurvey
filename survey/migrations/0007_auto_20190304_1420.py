# Generated by Django 2.1.7 on 2019-03-04 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_auto_20190304_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyemployee',
            name='endDatetime',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='surveyemployee',
            name='startDatetime',
            field=models.DateField(blank=True, null=True),
        ),
    ]
